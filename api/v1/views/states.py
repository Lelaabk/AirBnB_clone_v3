#!/usr/bin/python3
"""docs"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves list of all State objcts """
    states = storage.all(State).values()
    list_state = [state.to_dict() for state in states]
    return jsonify(list_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves State obj by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes State obj by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        state.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates new State obj """
    data = request.get_json()
    if not data:
        abort(404, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates State obj by ID """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    keys_ignored = ['id', 'created_at', 'updated_at']
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in keys_ignored:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
