#!/usr/bin/python3
"""Module for the city view"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models.city import City
import json

@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"])
def list_create_cities(state_id):
    """gets all cities or creates a new city in a given state"""
    if request.method == "GET":
        state = storage.get(State, state_id)
        cities_list = list()

        for city in state.cities:
            cities_list.append(city.to_dict())

        if state is None:
            abort(404)

        return cities_list, 200

    elif request.method == "POST":
        body = request.get_json()
        if not body:
            raise Exception(400, "Not a JSON")

        if "name" not in body:
            raise Exception(400, "Missing Name")

        body["state_id"] = state_id

        city = City(**body)
        city.save()

        return city.to_dict(), 201


@app_views.route("/cities/<city_id>/", methods=["GET", "DELETE", "PUT"])
def list_delete_update_city(city_id):
    """gets, deletes or updates a single city based on city_id"""
    city = storage.get(State, city_id)

    if city is None:
        abort(404)

    if request.method == "GET":
        return city.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(obj=city)
        storage.save()

        return {}, 200

    elif request.method == "PUT":
        body = request.get_json()

        if not body:
            raise Exception(400, "Not a JSON")

        for key, value in body.items():
            if key in ["id", "date_created", "updated_at"]:
                continue
            else:
                city.__setattr__(key, value)

        city.save()

        return city.to_dict(), 200
