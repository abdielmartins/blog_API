from typing import List, Tuple
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
    session = current_app.db.session

    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    posts_list: List[PostModel] = (
        session.query(PostModel)
        .join(UserModel)
        .filter(UserModel.id == user_id)
        .paginate(page=page, per_page=per_page, error_out=False)
        .items
    )

    print(posts_list.__dict__)

    return {
        "posts": [
            {"id": post.id, "nickname": user.nickname, "title": post.title, "content": post.content}
            for post, user in posts_list
        ]
    }, HTTPStatus.OK


@bp_post.route("/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    session = current_app.db.session
    found_post = PostModel.query.get(post_id)

    if not found_post:
        return {"message": "Post not found"}, HTTPStatus.NOT_FOUND

    session.delete(found_post)
    session.commit()

    return {"message": "Post successfully deleted"}, HTTPStatus.OK
