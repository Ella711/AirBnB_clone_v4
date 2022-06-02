#!/usr/bin/python3
""" index module for viewing request status  """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity,
           "cities": City,
           "places": Place,
           "reviews": Review,
           "states": State,
           "users": User}


@app_views.route('/status', methods=['GET'])
def status():
    """ view status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def cls_stats():
    """ view stats (count) for classes """
    cls_dict = {}
    for key, value in classes.items():
        cls_dict[key] = storage.count(value)

    return jsonify(cls_dict)
