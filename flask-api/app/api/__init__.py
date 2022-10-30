from app.database import db
from flask.blueprints import Blueprint

api_blueprint = Blueprint('api', __name__)

from .chord import *
from .song import *