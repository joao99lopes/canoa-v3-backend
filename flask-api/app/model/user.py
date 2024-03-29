import json
from datetime import datetime
from typing import List, Optional

from app.database import db
from app.model.playlist import Playlist
from app.model.relations import access, contribution
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = 'user'

    _id: int = db.Column('id', db.Integer, primary_key=True)

    _first_name: str = db.Column('first_name', db.String, nullable=False)
    _last_name: str = db.Column('last_name', db.String, nullable=False)

    _email: str = db.Column('email', db.String, nullable=False)
    _password: str = db.Column('password', db.String, nullable=False)  # TODO: save hashed pwd
    _verified_at: datetime = db.Column('verified_at', db.DateTime)
    _is_admin: bool = db.Column('is_admin', db.Boolean, default=False)

    _created_at: datetime = db.Column('created_at', db.DateTime, default=datetime.now)
    _updated_at: datetime = db.Column('updated_at', db.DateTime, onupdate=datetime.now)
    _deleted_at: datetime = db.Column('deleted_at', db.DateTime)

    _accesses = db.relationship("app.model.song.Song", secondary=access, back_populates='_accesses')
    _playlists = db.relationship("app.model.playlist.Playlist")
    _contributions = db.relationship("app.model.song.Song", secondary=contribution, back_populates='_contributions')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self._first_name = first_name
        self._last_name = last_name
        self._last_name = last_name
        self._email = email
        self._password = password
        self._is_admin = is_admin

    def __repr__(self):
        return {
            "id": self._id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email,
            "password": self._password,
            'verified_at': self._verified_at,
            'is_admin': self._is_admin,
            'accesses': self._accesses,
            "playlists": self._playlists,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
        }

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
    def accesses(self) -> Optional[access.__class__]:
        return self._accesses

    @hybrid_property
    def accesses_count(self) -> int:
        return len(self._accesses)

    @hybrid_property
    def playlists(self) -> List[Playlist.__class__]:
        return self._playlists

    @hybrid_property
    def contributions(self) -> List[contribution.__class__]:
        return self._contributions

    @hybrid_property
    def created_at(self) -> datetime:
        return self._created_at

    @hybrid_property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at

    @hybrid_property
    def deleted_at(self) -> Optional[datetime]:
        return self._deleted_at
