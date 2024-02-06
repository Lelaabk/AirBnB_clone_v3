#!/usr/bin/python3
""" Docs """

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """ Retrieves the list of all Place objects of city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object. """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """ Retrieves Place object based on provided JSON search critea """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if data is None or len(data) is None or (states is None and cities
                                             is None and amenities is None):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    list_places = []

    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]

        list_places = [place for place in list_places if
                       all([am in place.amenities for am in amenities_obj])]

    places = []
    for plc in list_places:
        dc = plc.to_dict()
        dc.pop('amenities', None)
        places.append(dc)

    return jsonify(places)
