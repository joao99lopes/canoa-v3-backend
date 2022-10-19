import json

from app.model import db

class Chord(db.Model):
    __tablename__ = "chords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    representation = db.Column(db.String(), nullable=False)
    is_minor = db.Column(db.Integer(), nullable=False)
#    image = db.Column(db.Image)??????  maybe url e depois saca a imagem a partir daí

    def __init__(self, name, is_minor, representation):
        self.name = name
        self.is_minor = is_minor
        self.representation = representation

    def __repr__(self):
        return json.dumps({
            "name": self.name,
            "is_minor": self.is_minor,
            "representation": self.representation
        })

