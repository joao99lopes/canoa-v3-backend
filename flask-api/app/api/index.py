from app.api import api_blueprint
from flask import jsonify

@api_blueprint.route('/')
def index_api():
    return jsonify("Hello World from the API!"), 200