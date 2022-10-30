from flask import Flask, jsonify
from flask_migrate import Migrate

from app.config import DBConfig
from app.database import db
from app.api import api_blueprint

app: Flask = None

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config.from_object(DBConfig)
    register_extensions(app)
    register_blueprints(app)
    return app 

def register_extensions(app):
    db.init_app(app)   
    
def register_blueprints(app):
    app.register_blueprint(api_blueprint, url_prefix='/api')

def setup_database(app):
    with app.app_context():
        db.create_all()
        db.session.commit()

app = create_app()
# setup_database(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify("Hello World!"), 200

# from app import models
#from app import api