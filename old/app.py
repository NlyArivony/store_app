from flask import Flask, request
from db import items, stores
from flask_smorest import abort
import uuid

app = Flask(__name__)

# stores = [{"name": "my store", "items": [{"name": "chair", "price": 15.99}]}]


@app.route("/")
def hello():
    return "Hello, World!"


@app.post("/store")
def create_store():
    """Create a store"""
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. ensure name is included in json payload.",
        )
    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message="Store already exist")
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.post("/item")
def create_item():
    """create an item"""
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. ensure price, store_id, and name are included in json payload.",
        )
    if item_data["store_id"] not in stores:
        # return {"message": "Store not found"}, 404
        abort(404, message="Store not found")
    for item in items.values():
        if item_data["name"] == item["name"]:
            abort(400, message="Item already exist")
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


@app.get("/store")
def get_stores():
    """Get all the stores in db"""
    return {"stores": list(stores.values())}


@app.get("/item")
def get_items():
    """Get all titems in db"""
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>/")
def get_store(store_id):
    """get a store"""
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    """get item"""
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found")


@app.delete(("/item/<string:item_id>"))
def delete_item(item_id):
    """delete item"""
    try:
        del items[item_id]
        return {"message": "Item deleted"}, 200
    except KeyError:
        abort(404, message="Item not found")


@app.delete(("/store/<string:store_id>"))
def delete_store(store_id):
    """delete store"""
    try:
        del stores[store_id]
        return {"message": "Store deleted"}, 200
    except KeyError:
        abort(404, message="Store not found")


@app.put(("/item/<string:item_id>"))
def update_item(item_id):
    """update item"""
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. ensure price and name are included in json payload.",
        )
    try:
        item = items[item_id]
        # item["name"] = item_data["name"]
        # item["price"] = item_data["price"]
        item |= item_data
        return item, 200

    except KeyError:
        abort(404, message="Item not found")


# if __name__ == "__main__":
#     app.run()
#     app.debug = True
