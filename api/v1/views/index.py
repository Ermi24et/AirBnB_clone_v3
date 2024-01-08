#!/usr/bin/python3
""" importing app_views and creating a route """

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ returns the status code """
    return {"status": "OK"}
