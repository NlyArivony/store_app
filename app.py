from flask import Flask, request
from db import items, stores
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
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.post("/store/item")
def create_item(name):
    """create an item"""
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    return new_item, 201


@app.get("/store")
def get_stores():
    """Get all the stores in db"""
    return {"stores": list(stores.values())}


@app.get("/item")
def get_stores():
    """Get all titems in db"""
    return {"items": list(items.values())}


@app.get("/store/<string:store_id>/")
def get_store(store_id):
    """get a store"""
    try:
        return stores[store_id], 200
    except KeyError:
        return {"message": "Store not found"}, 404


@app.get("/item/<string:item_id>")
def get_item(item_id):
    """get item in specific store"""
    try:
        return items[item_id], 200
    except KeyError:
        return {"message": "item not found"}, 404


# if __name__ == "__main__":
#     app.run()
#     app.debug = True
