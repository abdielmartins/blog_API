from flask import Blueprint, request, current_app
from blog.models.user_model import UserModel
from http import HTTPStatus

bp_user = Blueprint("user_view", __name__, url_prefix="/users")


@bp_user.route("", methods=["POST"])
def create_user():
    session = current_app.db.session

    body = request.get_json()

    nickname = body.get("nickname")
    email = body.get("email")
    password = body.get("password")

    new_user = UserModel(nickname=nickname, email=email)
    new_user.password = password
    session.add(new_user)
    session.commit()

    return {
        "user": {
            "nickname": nickname,
            "email": email,
        }
    }, HTTPStatus.CREATED


@bp_user.route("", methods=["GET"])
def list_users():
    username_filter = request.args.get("name")
    if username_filter:
        list_of_users = (
            UserModel.query.filter(UserModel.nickname.like(f"{username_filter}")).order_by(UserModel.nickname).all()
        )
    else:
        list_of_users = UserModel.query.all()

    return {
        "users": [{"id": user.id, "nickname": user.nickname, "email": user.email} for user in list_of_users]
    }, HTTPStatus.OK


@bp_user.route("/get/<int:user_id>", methods=["GET"])
def get_user(user_id):
    found_user = UserModel.query.get(user_id)

    if not found_user:
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    return {"user": {"id": found_user.id, "nickname": found_user.nickname, "email": found_user.email}}, HTTPStatus.OK


@bp_user.route("/<int:user_id>", methods=["PATCH", "PUT"])
def update_user(user_id):
    try:
        session = current_app.db.session

        body = request.get_json()

        email = body["email"]
        nickname = body["nickname"]

        found_user: UserModel = UserModel.query.get(user_id)
        found_user.email = email
        found_user.nickname = nickname

        session.add(found_user)
        session.commit()

        return {
            "user": {"id": found_user.id, "nickname": found_user.nickname, "email": found_user.email}
        }, HTTPStatus.OK

    except KeyError:
        return {"message": "Verify the request body"}, HTTPStatus.BAD_REQUEST
