#!/usr/bin/python3
"""endpoint for staatus"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exception):
    """Closes storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON-formatted 404 response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
