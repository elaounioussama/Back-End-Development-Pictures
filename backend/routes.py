from . import app
import os
import json
from flask import jsonify, request

# Load JSON data
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify({"status": "OK"}), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    if data:
        return jsonify({"length": len(data)}), 200
    return jsonify({"message": "Internal server error"}), 500


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE BY ID
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return jsonify({"message": "picture not found"}), 404


######################################################################
# CREATE A NEW PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    picture_in = request.json

    # Check if ID already exists
    for picture in data:
        if picture["id"] == picture_in["id"]:
            return jsonify({
                "message": f"picture with id {picture_in['id']} already present"
            }), 302

    data.append(picture_in)
    return jsonify(picture_in), 201


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_in = request.json

    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return jsonify(picture_in), 200   # Updated OK

    return jsonify({"message": "picture not found"}), 404


######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204  # No content

    return jsonify({"message": "picture not found"}), 404
