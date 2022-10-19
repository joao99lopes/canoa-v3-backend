import imp
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

from .song import *
from .chord import *
from .user import *
from .contribution import *
from .access import *