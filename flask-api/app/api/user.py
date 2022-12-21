from flask import request, jsonify
from flask.blueprints import Blueprint

from app.api import api_blueprint
from app.database import db
from app.model import User

user_blueprint = Blueprint('user', __name__)
api_blueprint.register_blueprint(user_blueprint, url_prefix='/user')


@user_blueprint.route('/', methods=['GET'])
def index():
    return jsonify(f"Hello World from /user!"), 200


# TODO: store password hash
@user_blueprint.route('/register', methods=['POST'])
def create_user():
    try:
        mandatory_fields = ['first_name', 'last_name', 'email', 'password']
        if not is_input_valid(request.json, mandatory_fields):
            return jsonify(error='Invalid input'), 403

        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']

        user: User = User.query.filter(User.email == email, User.deleted_at is None).first()
        if user is not None:
            return jsonify(error='Email already in use'), 403

        new_user = User(first_name, last_name, email, password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(data=new_user.__repr__()), 200
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418


@user_blueprint.route('/get', methods=['GET'])
def get_users():
    try:
        res = []
        users: list = User.query.all()
        for i in range(len(users)):
            res.append(users[i].__repr__())

        return jsonify(data=res), 200
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418


@user_blueprint.route('/get_by_id', methods=['GET'])
def get_user_by_id():
    try:
        mandatory_fields = ['id']
        if not is_input_valid(request.json, mandatory_fields):
            return jsonify(error='Invalid input'), 403

        user_id = request.json['id']
        user: list = User.query.filter_by(id=user_id).first()
        if user is None:
            return jsonify(error="No user with given id"), 403
        return jsonify(data=user.__repr__()), 200
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418


def is_input_valid(json, mandatory_fields):
    for field in mandatory_fields:
        if field not in list(json.keys()):
            return False
    return True
