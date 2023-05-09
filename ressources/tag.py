from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, TagAndItemSChema
from flask_jwt_extended import jwt_required
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import TagModel, StoreModel, ItemModel


blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Get tags of a store"""
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @jwt_required(fresh=True)
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    @blp.doc(security=[{"jwt": []}])
    def post(self, tag_data, store_id):
        """Create a tag in a store"""
        # if TagModel.query.filter(
        #     TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        # ).first():
        #     abort(400, message="A tag with that name already exist in that store.")

        new_tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(new_tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return new_tag


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """get a tag based on tag_id"""
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @jwt_required(fresh=True)
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted"},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    @blp.doc(security=[{"jwt": []}])
    def delete(self, tag_id):
        """delete a tag"""
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="COuld not delete tag. Make sure tag is not associated with any items, then try again.",
        )


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    """class to link or unlink tag and item"""

    @jwt_required(fresh=True)
    @blp.response(201, TagSchema)
    @blp.doc(security=[{"jwt": []}])
    def post(self, item_id, tag_id):
        "link an item from a tag"
        # check if item and tag id exist
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.qyery.get_or_404(tag_id)
        try:
            item.tags.append(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the tag.")

        return tag

    @jwt_required(fresh=True)
    @blp.response(200, TagAndItemSChema)
    @blp.doc(security=[{"jwt": []}])
    def delete(self, item_id, tag_id):
        """unlink item from a tag"""
        # check if item and tag id exist
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.qyery.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}
