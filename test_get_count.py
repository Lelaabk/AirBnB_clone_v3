#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.amenity import Amenity

print("All objects: {}".format(storage.count()))
print("Amenity objects: {}".format(storage.count(Amenity)))

first_state_id = list(storage.all(Amenity).values())[0].id
print("First amenity: {}".format(storage.get(Amenity, first_state_id)))