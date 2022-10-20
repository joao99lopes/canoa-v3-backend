from flask import Flask, jsonify
from flask_migrate import Migrate
from app.api import api_blueprint
from app.model import db
# creates an application that is named after the name of the file
app = Flask(__name__)

db_user = "postgres"
db_pw = "postgres"
db_host_ip = "postgres-db"
db_port = "5432"
db_name = "scoutify_db"
db_str = f"postgresql://{db_user}:{db_pw}@{db_host_ip}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_str

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api_blueprint, url_prefix='/api')

@app.route('/')
def index():
    return jsonify("Hello World!"), 200

from app import models
from app import api