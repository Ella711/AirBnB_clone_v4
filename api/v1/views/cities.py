#!/usr/bin/python3
""" cities module for viewing their request """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_by_state(state_id=None):
    """ view cities by state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_list = []
    cities = state.cities
    for city in cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def city_by_id(city_id=None):
    """ view city by id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """ delete a city by id """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id=None):
    """ returns a new city with status code 201 """
    requested_json = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")
    if "name" not in requested_json:
        abort(400, description="Missing name")
    requested_json["state_id"] = state_id
    new_city = City(**requested_json)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    """ update a city by id """
    city = storage.get(City, city_id)
    requested_json = request.get_json()
    if not city:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

    for key, value in requested_json.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
