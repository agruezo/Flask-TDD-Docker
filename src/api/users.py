from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from src.api.crud import (  # isort:skip
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    add_user,
    update_user,
    delete_user,
)

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class UsersList(Resource):
    @api.marshal_with(user, as_list=True)
    def get(self):

        return get_all_users(), 200

    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response = {}

        user = get_user_by_email(email)
        if user:
            response["message"] = "Sorry. That email already exists."
            return response, 400

        add_user(username, email)

        response["message"] = f"{email} was added!"

        return response, 201


class Users(Resource):
    @api.marshal_with(user)
    def get(self, user_id):
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        return user, 200

    @api.expect(user, validate=True)
    def put(self, user_id):
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response = {}

        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        if get_user_by_email(email):
            response["message"] = "Sorry. That email already exists."
            return response, 400

        update_user(user, username, email)

        response["message"] = f"{user.id} was updated!"

        return response, 200

    def delete(self, user_id):
        response = {}
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} does not exist")

        delete_user(user)

        response["message"] = f"{user.email} was removed!"

        return response, 200


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<int:user_id>")
