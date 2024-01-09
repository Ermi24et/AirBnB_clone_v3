#!/usr/bin/python3
"""
a new view for Place objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def place_list(city_id):
    """ retrieves the list of all Place objects """
    cities = storage.all("City").values()
    city_dict = [obj.to_dict() for obj in cities if obj.id == city_id]
    if city_dict == []:
        abort(404)
    places_list = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ retrieves Place object """
    places = storage.all("Place").values()
    place_dict = [obj.to_dict() for obj in places if obj.id == place_id]
    if place_dict == []:
        abort(404)
    return jsonify(place_dict[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ deletes a Place object """
    places = storage.all("Place").values()
    place_dict = [obj.to_dict() for obj in places if obj.id == place_id]
    if place_dict == []:
        abort(404)
    place_dict.remove(place_dict[0])
    for obj in places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ creates a Place object """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    cities = storage.all("City").values()
    city_dict = [obj.to_dict() for obj in cities
                 if obj.id == city_id]
    if city_dict == []:
        abort(404)
    places_list = []
    place_inst = Place(name=request.json['name'],
                       user_id=request.json['user_id'], city_id=city_id)
    users = storage.all("User").values()
    user_dict = [obj.to_dict() for obj in users
                 if obj.id == place_inst.user_id]
    if user_dict == []:
        abort(404)
    storage.new(place_inst)
    storage.save()
    places_list.append(place_inst.to_dict())
    return jsonify(places_list[0]), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ updates the Place object """
    places = storage.all("Place").values()
    place_dict = [obj.to_dict() for obj in places if obj.id == place_id]
    if place_dict == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' in request.get_json():
        place_dict[0]['name'] = request.json['name']
    if 'description' in request.get_json():
        place_dict[0]['description'] = request.json['description']
    if 'number_rooms' in request.get_json():
        place_dict[0]['number_rooms'] = request.json['number_rooms']
    if 'number_bathrooms' in request.get_json():
        place_dict[0]['number_bathrooms'] = request.json['number_bathrooms']
    if 'max_guest' in request.get_json():
        place_dict[0]['max_guest'] = request.json['max_guest']
    if 'price_by_night' in request.get_json():
        place_dict[0]['price_by_night'] = request.json['price_by_night']
    if 'latitude' in request.get_json():
        place_dict[0]['latitude'] = request.json['latitude']
    if 'longitude' in request.get_json():
        place_dict[0]['longitude'] = request.json['longitude']
    for obj in places:
        if obj.id == place_id:
            if 'name' in request.get_json():
                obj.name = request.json['name']
            if 'description' in request.get_json():
                obj.description = request.json['description']
            if 'number_rooms' in request.get_json():
                obj.number_rooms = request.json['number_rooms']
            if 'number_bathrooms' in request.get_json():
                obj.number_bathrooms = request.json['number_bathrooms']
            if 'max_guest' in request.get_json():
                obj.max_guest = request.json['max_guest']
            if 'price_by_night' in request.get_json():
                obj.price_by_night = request.json['price_by_night']
            if 'latitude' in request.get_json():
                obj.latitude = request.json['latitude']
            if 'longitude' in request.get_json():
                obj.longitude = request.json['longitude']
    storage.save()
    return jsonify(place_dict[0]), 200
