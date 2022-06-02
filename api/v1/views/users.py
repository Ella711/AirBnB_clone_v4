#!/usr/bin/python3
""" users module for viewing their requests """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ view all users """
    all_users = storage.all(User).values()
    users_list = []
    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def user_by_id(user_id=None):
    """ view user by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """ delete a user by id """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """ returns a new user with status code 201 """
    requested_json = request.get_json()
    if not requested_json:
        abort(400, description="Not a JSON")
    if "email" not in requested_json:
        abort(400, description="Missing email")
    if "password" not in requested_json:
        abort(400, description="Missing password")
    new_user = User(**requested_json)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """ update a user by id """
    user = storage.get(User, user_id)
    requested_json = request.get_json()
    if not user:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in requested_json.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
