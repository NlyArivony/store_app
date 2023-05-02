import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """get a store"""
        try:
            # return stores[store_id], 200
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    @blp.response(200)
    def delete(self, store_id):
        """delete store"""
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """Get all the stores in db"""
        # return {"stores": list(stores.values())}
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        """Create a store"""

        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(
        #         400,
        #         message="Bad request. ensure name is included in json payload.",
        #     )

        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, message="Store already exist")
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store
