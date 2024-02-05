#!/usr/bin/python3
""" docs"""
import os
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity

db_storage = os.getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """ retrive place amenities based on place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if db_storage == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [amenity.to_dict() for amenity in place.amenities_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """ delete amenity from place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if db_storage == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenities_ids:
            abort(404)
        place.amenities_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def create_amenity(place_id, amenity_id):
    """ create amenity for place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if db_storage == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenities_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenities_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
