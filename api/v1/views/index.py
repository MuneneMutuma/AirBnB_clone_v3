#!/usr/bin/python3
"""Index page for views"""


from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models.state import State

classes = {
        "amenities": Amenity,
        "places": Place,
        "cities": City,
        "users": User,
        "reviews": Review,
        "states": State
        }


@app_views.route("/status/")
def status():
    """Gets status of API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats/")
def stats():
    """Gets statistics of objects of each type by count"""
    statistics = dict()
    for cls, obj in classes.items():
        statistics[cls] = storage.count(obj)

    return jsonify(statistics)
