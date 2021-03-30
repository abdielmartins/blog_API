from flask import Blueprint, request, current_app
from http import HTTPStatus

from blog.models.user_model import UserModel
from blog.models.post_model import PostModel

bp_post = Blueprint("post_view", __name__, url_prefix="/posts")


@bp_post.route("/<int:user_id>", methods=["POST"])
def create_post(user_id):
    session = current_app.db.session

    body = request.get_json()
    title = body.get("title")
    content = body.get("content")
    found_user = UserModel.query.get(user_id)

    if not found_user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    new_post = PostModel(title=title, content=content)

    found_user.post_list.append(new_post)
    session.add(found_user)
    session.commit()

    return {"post": {"id": new_post.id, "title": new_post.title, "content": new_post.content}}, HTTPStatus.CREATED


@bp_post.route("/list/<int:user_id>", methods=["GET"])
def list_user_posts(user_id):
    found_user = UserModel.query.get(user_id)

    if not found_user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    user_posts = found_user.post_list

    return {"posts": [{"title": post.title, "content": post.content} for post in user_posts]}, HTTPStatus.OK


@bp_post.route("/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    session = current_app.db.session
    found_post = PostModel.query.get(post_id)

    if not found_post:
        return {"message": "Post not found"}, HTTPStatus.NOT_FOUND

    session.delete(found_post)
    session.commit()

    return {"message": "Post successfully deleted"}, HTTPStatus.OK
