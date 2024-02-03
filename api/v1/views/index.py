#!/usr/bin/python3
"""rout blueprints"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON response with status OK"""
    return jsonify({"status": "OK"})