from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.hybrid import hybrid_property
import json

from app.model import db, Song, Access, Contribution


class User(db.Model):
    __tablename__ = "user"

    _id = db.Column(db.Integer, primary_key=True)
    
    _first_name = db.Column(db.String, nullable=False)
    _last_name = db.Column(db.String, nullable=False)
    _username = db.Column(db.String, unique=True, nullable=False)
    
    _email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.String, nullable=False)    #TODO: save hashed pwd
    _verified_at = db.Column(db.DateTime)
    
    _is_admin = db.Column(db.Boolean, default=False)

    _accesses = db.relationship(Song.__name__, secondary=Access, backref='_accesses')
    _playlists = db.Column(db.JSON) # relationship user-song
    _contributions = db.relationship(Song.__name__, secondary=Contribution, backref='_contributions')
    
    _created_at = db.Column(db.DateTime, default=datetime.now)
    _updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, 
                 first_name, 
                 last_name, 
                 username, 
                 email, 
                 password, 
                 is_admin = False, 
                 verified_at = None, 
                 accesses = None, 
                 playlists = None, 
                 contributions = None, 
                 created_at = datetime.now(), 
                 updated_at = datetime.now()):
        
        self._first_name = first_name
        self._last_name = last_name
        self._last_name = last_name
        self._username = username
        self._email = email
        self._password = password
        self._verified_at = verified_at
        self._is_admin = is_admin
        self._accesses = accesses
        self._playlists = playlists
        self._contributions = contributions
        self._created_at = created_at
        self._updated_at = updated_at


    def verified_at_repr(self) -> str:
        if self._verified_at is not None:
            self._verified_at.strftime("%d-%m-%Y %H:%M")
        return self._verified_at
        
        
    def __repr__(self):
        return json.dumps({
            "id": self._id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "username": self._username,
            "email": self._email,
            "password": self._password,
            'verified_at': self.verified_at_repr(),
            'is_admin': self._is_admin,
            'accesses': self._accesses,
            "playlists": self._playlists,
            "created_at": self._created_at.strftime("%d-%m-%Y %H:%M"),
            "updated_at": self._updated_at.strftime("%d-%m-%Y %H:%M"),
        })

    @hybrid_property
    def id(self) -> int:
        return self._id
    
    @hybrid_property
    def first_name(self) -> str:
        return self._first_name
    
    @hybrid_property
    def last_name(self) -> str:
        return self._last_name
    
    @hybrid_property
    def username(self) -> str:
        return self._username
    
    @hybrid_property
    def email(self) -> str:
        return self._email
    
    @hybrid_property
    def password(self) -> str:
        return self._password
    
    @hybrid_property
    def verified_at(self) -> Optional[datetime]:
        return self._verified_at
    
    @hybrid_property
    def is_verified(self) -> bool:
        return self._verified_at is not None
        
    @hybrid_property
    def is_admin(self) -> bool:
        return self._is_admin
    
    @hybrid_property
    def accesses(self) -> Optional[Access.__class__]:
        return self._accesses
    
    @hybrid_property
    def accesses_count(self) -> int:
        return len(self._accesses)

    @hybrid_property
    def playlists(self) -> List[Playlist.__class__]:
        return self._playlists

    @hybrid_property
    def contributions(self) -> List[Contribution.__class__]:
        return self._contributions
    

    @hybrid_property
    def created_at(self) -> Optional[datetime]:
        return self._created_at
    
    @hybrid_property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at
    

