from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from flask_jwt_extended import jwt_required
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import StoreModel


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """get a store"""
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required(fresh=True)
    @blp.response(200)
    @blp.doc(security=[{"jwt": []}])
    def delete(self, store_id):
        """delete store"""
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}
        # raise NotImplementedError("Deleteing a store is not implemented.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Get all the stores in db"""
        return StoreModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    @blp.doc(security=[{"jwt": []}])
    def post(self, store_data):
        """Create a store"""
        new_store = StoreModel(**store_data)

        try:
            db.session.add(new_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting new item.")

        return new_store
