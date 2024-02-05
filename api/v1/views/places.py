#!/usr/bin/python3
""" Docs """

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """ Retrieves the list of all Place objects """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object. """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes a Place object. """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object. """
    data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(400)

    if data is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    if 'name' not in data:
        abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    # Here assign city_id to JSON data
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object. """
    place = storage.get(Place, place_id)
    data = request.get_json()
    if place:
        if data is None:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ('id', 'user_id', 'city_id',
                           'created_at', 'updated_at'):
                setattr(place, key, value)

        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
