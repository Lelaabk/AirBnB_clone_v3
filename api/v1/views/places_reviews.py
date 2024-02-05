#!/usr/bin/python3
""" Docs """

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Reviews objects of Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object. """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a Review object. """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('//places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review object. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')

    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    if 'text' not in data:
        abort(400, 'Missing text')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object. """
    review = storage.get(Review, review_id)
    data = request.get_json()
    if review:
        if data is None:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ('id', 'user_id', 'place_id', 'created_at',
                           'updated_at'):
                setattr(review, key, value)

        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
