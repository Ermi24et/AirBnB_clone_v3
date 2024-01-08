#!/usr/bin/python3
""" importing app_views and creating a route """

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class_dict = {"amenities": "Amenity", "cities": "City", "places": "Place",
              "reviews": "Review", "states": "State", "users": "User"}


@app_views.route('/status')
def status():
    """ returns the status code """
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """ an endpoint retrieves the number of each objects by type """
    new_dict = {}
    for key in class_dict:
        new_dict[key] = storage.count(class_dict[key])
    return new_dict
