#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_list(state_id):
    """ retrieves State object """
    states = storage.all("State").values()
    state_dict = [obj.to_dict() for obj in states if obj.id == state_id]
    if state_dict == []:
        abort(404)
    cities_list = [obj.to_dict() for obj in storage.all("City").values()
                   if state_id == obj.state_id]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ retrieves the list of all state objects """
    cities = storage.all("City").values()
    city_dict = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city_dict == []:
        abort(404)
    return jsonify(city_dict[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ deletes a city object """
    cities = storage.all("City").values()
    city_dict = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city_dict == []:
        abort(404)
    city_dict.remove(city_dict[0])
    for obj in cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ creates a State object """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = storage.all("State").values()
    state_dict = [obj.to_dict() for obj in states if obj.id == state_id]
    if state_dict == []:
        abort(404)
    cities = []
    city_inst = City(name=request.json['name'], state_id=state_id)
    storage.new(city_inst)
    storage.save()
    cities.append(city_inst.to_dict())
    return jsonify(cities[0]), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ updates the State object """
    cities = storage.all("City").values()
    city_dict = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city_dict == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city_dict[0]['name'] = request.json['name']
    for obj in cities:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(city_dict[0]), 200
