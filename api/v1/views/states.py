#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def state_list():
    """ retrieves the list of all state objects """
    state_list = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ retrieves State object """
    states = storage.all("State").values()
    state_dict = [obj.to_dict() for obj in states if obj.id == state_id]
    if state_dict == []:
        abort(404)
    return jsonify(state_dict[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ deletes a state object """
    states = storage.all("State").values()
    state_dict = [obj.to_dict() for obj in states if obj.id == state_id]
    if state_dict == []:
        abort(404)
    state_dict.remove(state_dict[0])
    for obj in states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    """ creates a State object """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states_list = []
    state_inst = State(name=request.json['name'])
    storage.new(state_inst)
    storage.save()
    states_list.append(state_inst.to_dict())
    return jsonify(states_list[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ updates the State object """
    states = storage.all("State").values()
    state_dict = [obj.to_dict() for obj in states if obj.id == state_id]
    if state_dict == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_dict[0]['name'] = request.json['name']
    for obj in states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_dict[0]), 200
