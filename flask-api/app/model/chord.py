import json
from sqlalchemy.ext.hybrid import hybrid_property

from app.model import db

class Chord(db.Model):
    __tablename__ = "chords"

    _id: int = db.Column('id', db.Integer, primary_key=True)
    _name: str = db.Column('name', db.String, nullable=False)
    _representation: str = db.Column('representation', db.String, nullable=False)
    _is_minor: int = db.Column('is_minor', db.Boolean, nullable=False)
#    image = db.Column(db.Image)??????  maybe url e depois saca a imagem a partir daí

    def __init__(self, name, is_minor, representation):
        self._name = name
        self._is_minor = is_minor
        self._representation = representation

    def __repr__(self):
        return json.dumps({
            "name": self._name,
            "is_minor": self._is_minor,
            "representation": self._representation
        })
        
    @hybrid_property
    def id(self) -> int:
        return self._id
    
    @hybrid_property
    def name(self) -> str:
        return self._name
    
    @hybrid_property
    def representation(self) -> str:
        return self._representation
    
    @hybrid_property
    def is_minor(self) -> bool:
        return self._is_minor

