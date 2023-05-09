from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import UserModel
from schemas import UserSchema

from blocklist import BLOCKLIST

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/register/")
class UserRegister(MethodView):
    @jwt_required(fresh=True)
    @blp.arguments(UserSchema)
    @blp.doc(security=[{"jwt": []}])
    def post(self, user_data):
        """register a user if logged in user is admin"""
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message=" A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """get user by user_id"""
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required(fresh=True)
    @blp.doc(security=[{"jwt": []}])
    def delete(self, user_id):
        """delete user based on user_id if logged in user is admin"""
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "user deleted."}, 200


@blp.route("/login/")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """create access token"""
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="Invalid credentials.")


@blp.route("/refresh/")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    @blp.doc(security=[{"jwt": []}])
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout/")
class UserLogout(MethodView):
    @jwt_required()
    @blp.doc(security=[{"jwt": []}])
    def post(sef):
        """func that grab the jti and add it to the blocklist"""
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}
