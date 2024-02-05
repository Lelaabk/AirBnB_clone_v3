#!/usr/bin/python3
"""rout blueprints"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON response with status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False, methods=["GET"])
def stats():
    """Retrieves the number of each object type"""
    amenities = storage.count(Amenity)
    cities = storage.count(City)
    users = storage.count(User)
    places = storage.count(Place)
    reviews = storage.count(Review)
    states = storage.count(State)

    return {
        "amenities": amenities,
        "cities": cities,
        "users": users,
        "places": places,
        "reviews": reviews,
        "states": states
    }
