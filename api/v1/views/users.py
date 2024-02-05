#!/usr/bin/python3
""" Docs """

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object. """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a User object. """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Creates a User object. """
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Updates User object. """
    user = storage.get(User, user_id)
    data = request.get_json()
    if user:
        if data is None:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ('id', 'email', 'created_at', 'updated_at'):
                setattr(user, key, value)

        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
