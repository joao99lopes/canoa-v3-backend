from operator import imod
from flask import Blueprint
api_blueprint = Blueprint('api', __name__)

from .index import *
from .chord import *
