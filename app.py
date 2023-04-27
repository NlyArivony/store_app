from flask import Flask, request

app = Flask(__name__)

stores = [{"name": "my store", "items": [{"name": "chair", "price": 15.99}]}]


@app.route("/")
def hello():
    return "Hello, World!"


@app.post("/store")
def create_store():
    """Create a store"""
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": request_data["items"]}
    stores.append(new_store)
    return new_store, 201


@app.get("/store")
def get_stores():
    """Get all the stores in db"""
    return {"stores": stores}


@app.get("/store/<string:name>/")
def get_items_in_store(name):
    """get the details in a store"""
    for store in stores:
        if store["name"] == name:
            return store, 200
    return {"message": "Store not found"}, 404


@app.post("/store/<string:name>/item")
def create_item(name):
    """create an item based on a store name"""
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


if __name__ == "__main__":
    app.run()
    app.debug = True
