#!/usr/bin/python3
"""
a new view for User objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def state_list():
    """ retrieves the list of all user objects """
    users_list = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ retrieves User object """
    users = storage.all("User").values()
    user_dict = [obj.to_dict() for obj in users if obj.id == user_id]
    if user_dict == []:
        abort(404)
    return jsonify(user_dict[0])


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ deletes a user object """
    users = storage.all("User").values()
    user_dict = [obj.to_dict() for obj in users if obj.id == user_id]
    if user_dict == []:
        abort(404)
    user_dict.remove(user_dict[0])
    for obj in users:
        if obj.id == user_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    """ creates a User object """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing name')
    if 'password' not in request.get_json():
        abort(400, 'Missing name')
    users = []
    user_inst = User(email=request.json['email'],
                     password=request.json['password'])
    storage.new(user_inst)
    storage.save()
    users.append(user_inst.to_dict())
    return jsonify(users[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ updates the User object """
    users = storage.all("User").values()
    user_dict = [obj.to_dict() for obj in users if obj.id == user_id]
    if user_dict == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user_dict[0]['first_name'] = request.json['first_name']
    except Exception:
        pass
    try:
        user_dict[0]['last_name'] = request.json['last_name']
    except Exception:
        pass

    for obj in users:
        if obj.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    obj.first_name = request.json['first_name']
            except Exception:
                pass
            try:
                if request.json['last_name'] is not None:
                    obj.last_name = request.json['last_name']
            except Exception:
                pass
    storage.save()
    return jsonify(user_dict[0]), 200
