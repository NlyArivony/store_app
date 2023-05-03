from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema

from db import db
from sqlalchemy.exc import SQLAlchemyError
from models import TagModel, StoreModel

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Get tags of a store"""
        store = StoreModel.guery.get_or_404(store_id)

        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
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


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
