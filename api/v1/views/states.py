#!/usr/bin/python3
"""Module for the state view"""

from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
import json

@app_views.route("/states/", methods=["GET", "POST"])
def list_create_states():
    """gets all states or creates a new state"""
    if request.method == "GET":
        states = storage.all(State)
        dict_states = list()

        if states is None:
            abort(404)

        for key, state in states.items():
            dict_states.append(state.to_dict())

        return json.dumps(dict_states), 200

    elif request.method == "POST":
        body = request.get_json()
        if not body:
            raise Exception(400, "Not a JSON")

        if "name" not in body:
            raise Exception(400, "Missing Name")

        state = State(**body)

        state.save()

        return state.to_dict(), 201
@app_views.route("/states/<state_id>/", methods=["GET", "DELETE", "PUT"])
def list_delete_update_state(state_id):
    """gets, deletes or updates a single state based on state_id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == "GET":
        return state.to_dict(), 200

    elif request.method == "DELETE":
        storage.delete(obj=state)
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
                state.__setattr__(key, value)

        state.save()

        return state.to_dict(), 200
