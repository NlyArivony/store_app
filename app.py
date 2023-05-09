import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
import models
from ressources.item import blp as ItemBlueprint
from ressources.store import blp as StoreBlueprint
from ressources.tag import blp as TagBlueprint
from ressources.user import blp as UserBlueprint


def create_app(db_url=None):
    """function to create and setup a flask app"""
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)

    api = Api(app)

    # create an instance of jwt manager
    app.config["JWT_SECRET_KEY"] = "208325419217662809979992809858158591106"
    jwt = JWTManager(app)

    # add addtional information to jwt (func that run for access token creation)
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """add addtional information to jwt for each token creation)"""
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    # overiding jwt error
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # create table before any request to the api
    @app.before_request
    def create_table():
        """function that create table before request to the flask app"""
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    # Define the Swagger specification
    api.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )

    return app
