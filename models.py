from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class InfoModel(db.Model):
    __tablename__ = 'info_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    age = db.Column(db.Integer())
    password = db.Column(db.String())
    email = db.Column(db.String(), unique=True)

    def __init__(self, name, age, email, password):
        self.name = name
        self.age = age
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.name}:{self.age}"