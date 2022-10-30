from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from typing import List
import json

from app.database import db

user_fk = "user.id"
song_fk = "song.id"

class Playlist(db.Model):
    __tablename__ = 'playlist'
    _id = db.Column('id', db.Integer, primary_key=True)
    _name = db.Column('name', db.String, nullable=False)
    _user_id = db.Column('user_id', db.Integer, db.ForeignKey(user_fk), nullable=False)
    _song_ids = db.Column('song_ids', db.ARRAY(db.Integer, db.ForeignKey(song_fk)))
    _created_at = db.Column('created_at', db.Datetime, default=datetime.now)
    _updated_at = db.Column('updated_at', db.Datetime, default=datetime.now, onupdate=datetime.now)
    _deleted_at = db.Column('deleted_at', db.Datetime)
    

    def __init__(self, name, user_id):
        self._name = name
        self._user_id = user_id
        
    def __repre__(self):
        return json.dumps({
            'id': self._id,
            'name': self._name,
            'user_id': self._user_id,
            'song_ids': self._song_ids,
            'created_at': self._created_at,
            'updated_at': self._updated_at,
            'deleted_at': self._deleted_at,
        })
        
    @hybrid_property
    def id(self) -> int:
        return self.id
    
    @hybrid_property
    def name(self) -> str:
        return self.name

    @hybrid_property
    def user_id(self) -> int:
        return self.user_id

    @hybrid_property
    def song_ids(self) -> List[int]:
        return self.id
    
    @hybrid_property
    def created_at(self) -> datetime:
        return self._created_at

    @hybrid_property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    @hybrid_property
    def deleted_at(self) -> datetime:
        return self._deleted_at

