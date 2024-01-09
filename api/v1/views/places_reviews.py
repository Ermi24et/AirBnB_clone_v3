#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def reviews_list(place_id):
    """ retrieves the list of all Review objects """
    places = storage.all("Place").values()
    place_dict = [obj.to_dict() for obj in places if obj.id == place_id]
    if place_dict == []:
        abort(404)
    reviews_list = [obj.to_dict() for obj in storage.all("Review").values()
                    if place_id == obj.place_id]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ retrieves Review object """
    reviews = storage.all("Review").values()
    review_dict = [obj.to_dict() for obj in reviews if obj.id == review_id]
    if review_dict == []:
        abort(404)
    return jsonify(review_dict[0])


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ deletes a Review object """
    reviews = storage.all("Review").values()
    review_dict = [obj.to_dict() for obj in reviews if obj.id == review_id]
    if review_dict == []:
        abort(404)
    review_dict.remove(review_dict[0])
    for obj in reviews:
        if obj.id == review_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ creates a Review object """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    places = storage.all("Place").values()
    place_dict = [obj.to_dict() for obj in places if obj.id == place_id]
    if place_dict == []:
        abort(404)
    users = storage.all("User").values()
    user_dict = [obj.to_dict() for obj in users if obj.id == user_id]
    if user_dict == []:
        abort(404)
    reviews = []
    review_inst = Review(text=request.json['text'], place_id=place_id,
                         user_id=user_id)
    storage.new(review_inst)
    storage.save()
    reviews.append(review_inst.to_dict())
    return jsonify(reviews_list[0]), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ updates the Review object """
    reviews = storage.all("Review").values()
    review_dict = [obj.to_dict() for obj in reviews if obj.id == review_id]
    if review_dict == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' in request.get_json():
        review_dict[0]['text'] = request.json['text']
        for obj in reviews:
            if obj.id == review_id:
                obj.text = request.json['text']
        storage.save()
    return jsonify(review_dict[0]), 200
