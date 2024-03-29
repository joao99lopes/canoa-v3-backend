import json
from datetime import datetime
from typing import List, Optional

from app.database import db
from app.model.relations import access, contribution
from sqlalchemy.ext.hybrid import hybrid_property

user_fk: str = 'user.id'


class Song(db.Model):
    __tablename__ = 'song'

    _id: int = db.Column('id', db.Integer, primary_key=True)
    
    _title: str = db.Column('title', db.String, unique=True, nullable=False)
    _lyrics: str = db.Column('lyrics', db.ARRAY(db.String), nullable=False)
    _creator_id: int = db.Column('creator_id', db.Integer, db.ForeignKey(user_fk), nullable=False)
    _verified_at: datetime = db.Column('verified_at', db.DateTime)
    
    _chords = db.Column('chords', db.JSON)    # TODO: fix chords
    _categories: List[str] = db.Column('categories', db.ARRAY(db.String))

    _created_at: datetime = db.Column('created_at', db.DateTime, default=datetime.now)
    _updated_at: datetime = db.Column('updated_at', db.DateTime, onupdate=datetime.now)
    _deleted_at: datetime = db.Column('deleted_at', db.DateTime)
    
    # TODO: turn this into relationships
    _contributions = db.relationship("app.model.user.User", secondary=contribution, back_populates='_contributions')
    _accesses = db.relationship("app.model.user.User", secondary=access, back_populates='_accesses')

    def __init__(self, 
                 title, 
                 lyrics, 
                 creator_id, 
                 chords = None, 
                 categories = None):
        
        self._title = title
        self._lyrics = lyrics
        self._creator_id = creator_id
        self._chords = chords
        self._categories = categories


    def __repr__(self):
        return {
            "id": self._id,
            "title": self._title,
            "lyrics": self._lyrics,
            "chords": self._chords,
            "categories": self._categories,
            "creator_id": self._creator_id,
            "verified_at": self._verified_at,
            "created_at": self._created_at,
            "updated_at": self._updated_at,
            "deleted_at": self._deleted_at,
            "contributions": self._contributions,
            "accesses": self._accesses,
        }
        
    @hybrid_property
    def id(self) -> int:
        return self._id
    
    @hybrid_property
    def title(self) -> str:
        return self._title
    
    @hybrid_property
    def lyrics(self) -> List[str]:
        return self._lyrics
    
    @hybrid_property
    def creator_id(self) -> int:
        return self._creator_id
    
    @hybrid_property
    def verified_at(self) -> Optional[datetime]:
        return self._verified_at
    
    @hybrid_property
    def is_verified(self) -> bool:
        return self._verified_at is not None
        
    @hybrid_property
    def chords(self) -> dict:
        return self._chords
    
    @hybrid_property
    def categories(self) -> List[str]:
        return self._categories

    @hybrid_property
    def created_at(self) -> datetime:
        return self._created_at
    
    @hybrid_property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at
    
    @hybrid_property
    def contributions(self) -> List[contribution.__class__]:
        return self._contributions
    
    @hybrid_property
    def accesses(self) -> List[access.__class__]:
        return self._accesses
        
    @hybrid_property
    def accesses_count(self) -> int:
        return len(self._accesses)
    
    

    
    
    