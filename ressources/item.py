from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema

from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel

from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """get item"""
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required(fresh=True)
    @blp.response(200)
    @blp.doc(security=[{"jwt": []}])
    def delete(self, item_id):
        """check if logged user is admin to perform the delete item based on item_id"""
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Store deleted"}

        # raise NotImplementedError("Deleteing an item is not implemented.")

    @jwt_required(fresh=True)
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    @blp.doc(security=[{"jwt": []}])
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

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    @blp.doc(security=[{"jwt": []}])
    def post(self, item_data):
        """create an item"""
        new_item = ItemModel(**item_data)

        try:
            db.session.add(new_item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting new item.")

        return new_item
