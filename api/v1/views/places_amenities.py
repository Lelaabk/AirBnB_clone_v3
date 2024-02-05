#!/usr/bin/python3
"""Handles RESTful API actions for State objects."""
import os
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place

db_mode = os.getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def get_place_amenities(place_id):
    """Retrieve amenities for a place."""
    amenities_list = []
    place = storage.get(Place, place_id)
    if not place:
        abort(400)

    if db_mode == "db":
        amenities_list = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities_list = place.amenity_ids

    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(place_id, amenity_id):
    """Delete an amenity by ID."""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if db_mode == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id

    for place_amenity in place_amenities:
        if place_amenity.id == amenity_id:
            place_amenity.delete()
            place_amenity.save()
            return jsonify({}), 200

    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["POST"])
def link_amenity(place_id, amenity_id):
    """Link an Amenity to a Place."""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if db_mode == "db":
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities_id

    if amenity not in place_amenities:
        place_amenities.append(amenity)
        return jsonify(amenity.to_dict()), 201

    return jsonify(amenity.to_dict()), 200
