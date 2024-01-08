#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from models.state import State


@app_views.route('/amenities/', methods=['GET'])
def amenities_list():
    """ retrieves the list of all Amenity objects """
    amenities_list = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ retrieves State object """
    amenities = storage.all("Amenity").values()
    amenities_dict = [obj.to_dict() for obj in amenities
                      if obj.id == amenity_id]
    if amenity_dict == []:
        abort(404)
    return jsonify(amenity_dict[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ deletes a state object """
    amenities = storage.all("Amenity").values()
    amenity_dict = [obj.to_dict() for obj in amenities if obj.id == amenity_id]
    if amenity_dict == []:
        abort(404)
    amenity_dict.remove(state_dict[0])
    for obj in amenities:
        if obj.id == amenity_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    """ creates a State object """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    amenity_inst = Amenity(name=request.json['name'])
    storage.new(amenity_inst)
    storage.save()
    amenities.append(amenity_inst.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ updates the State object """
    amenities = storage.all("Amenity").values()
    amenity_dict = [obj.to_dict() for obj in amenities if obj.id == amenity_id]
    if amenity_dict == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity_dict[0]['name'] = request.json['name']
    for obj in amenities:
        if obj.id == amenity_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(amenity_dict[0]), 200
