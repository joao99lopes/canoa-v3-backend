from flask import request, render_template, jsonify
import json
from flask.blueprints import Blueprint
#from pydantic import BaseModel

from app.api import api_blueprint
from app.database import db
from app.model import User

user_blueprint = Blueprint('user', __name__)
api_blueprint.register_blueprint(user_blueprint, url_prefix='/user')

@user_blueprint.route('/', methods=['GET'])
def index():
    return jsonify(f"Hello World from /user!"), 200

@user_blueprint.route('/new', methods=['GET'])
def create_user():
    first_name = 'joao'
    last_name = 'lopes'
    username = 'lopesj99as'
    email = 'joao@test.paat'
    password = '123123'
    is_admin = True
    new_user = User(first_name, last_name, username, email, password, is_admin)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(data=new_user.__repr__()), 200


@user_blueprint.route('/fetch', methods=['GET'])
def get_users():
    res = []
    users : list = User.query.all()
    if len(users) == 0:
        return jsonify(error="No users"), 406
    for i in range(len(users)):
        res.append(users[i].__repr__())
    
    return jsonify(data=res), 200

