from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema

from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """get item"""
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.response(200)
    def delete(self, item_id):
        """delete item"""
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Store deleted"}

        # raise NotImplementedError("Deleteing an item is not implemented.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """update item"""
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

        # raise NotImplementedError("updating an item is not implemented.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """Get all items in db"""
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """create an item"""
        new_item = ItemModel(**item_data)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting new item.")

        return new_item
