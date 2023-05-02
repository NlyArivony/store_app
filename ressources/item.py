import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """get item"""
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item not found")

    @blp.response(200)
    def delete(self, item_id):
        """delete item"""
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """update item"""

        # item_data = request.get_json()
        # if "price" not in item_data or "name" not in item_data:
        #     abort(
        #         400,
        #         message="Bad request. ensure price and name are included in json payload.",
        #     )

        try:
            item = items[item_id]
            # item["name"] = item_data["name"]
            # item["price"] = item_data["price"]
            item |= item_data
            return item

        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Get all items in db"""
        # return {"items": list(items.values())}
        # return a list of item
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """create an item"""

        # item_data = request.get_json()
        # if (
        #     "price" not in item_data
        #     or "store_id" not in item_data
        #     or "name" not in item_data
        # ):
        #     abort(
        #         400,
        #         message="Bad request. ensure price, store_id, and name are included in json payload.",
        #     )

        if item_data["store_id"] not in stores:
            # return {"message": "Store not found"}, 404
            abort(404, message="Store not found")
        for item in items.values():
            if item_data["name"] == item["name"]:
                abort(400, message="Item already exist")
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item
        # return new_item, 201
        return new_item
