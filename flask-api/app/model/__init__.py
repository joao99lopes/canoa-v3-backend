import imp
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

from .song import *
from .chord import *
from .user import *
from .relations import *
from .playlist import *