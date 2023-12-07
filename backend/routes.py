from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture

    return make_response({"message": "Not found"}, 404)

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    json_req = request.get_json()

    for picture in data:
        if picture["id"] == json_req["id"]:
            return make_response({"Message": f"picture with id {picture['id']} already present"}, 302)

    data.append(json_req)
    return make_response(json_req, 201)

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    json_req = request.get_json()

    for i, picture in enumerate(data):
        if picture["id"] == id:
            data[i] = json_req
            return make_response({"Message": "Picture updated"}, 200)

    return make_response({"message": "Not found"}, 404) 

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    for i, picture in enumerate(data):
        if picture["id"] == id:
            del data[i]
            return make_response({"Message": "Picture deleted"}, 204)

    return make_response({"message": "Not found"}, 404) 
