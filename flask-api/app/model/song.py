import json
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List, Optional

from app.model import db, User, Access, Contribution

user_fk: str = f'{User.__tablename__}.id'


class Song(db.Model):
    __tablename__ = "song"

    _id = db.Column(db.Integer, primary_key=True)
    
    _title = db.Column(db.String, unique=True, nullable=False)
    _lyrics = db.Column(db.ARRAY(db.String), nullable=False)
    _creator_id = db.Column(db.Integer, nullable=False)
    
    _verified_at = db.Column(db.DateTime)
    
    # TODO: this might be better as relationships (?)
    _chords = db.Column(db.JSON)
    _categories = db.Column(db.ARRAY(db.String))

    _created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    _updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # TODO: turn this into relationships
    _contributions = db.relationship(User.__name__, secondary=Contribution, backref='_contributions')
    _accesses = db.relationship(User.__name__, secondary=Access, backref='_accesses')

    def __init__(self, 
                 title, 
                 lyrics, 
                 creator_id, 
                 verified_at = None, 
                 chords = None, 
                 categories = None,
                 contributions = None,
                 accesses = None):
        
        self._title = title
        self._lyrics = lyrics
        self._creator_id = creator_id
        self._verified_at = verified_at
        self._chords = chords
        self._categories = categories
        self._contributions = contributions
        self._accesses = accesses

    def __repr__(self):
        return json.dumps({
            "id": self._id,
            "title": self._title,
            "lyrics": self._lyrics,
            "chords": self._chords,
            "categories": self._categories,
            "creator_id": self._creator_id,
            "verified_at": self._verified_at.strftime("%d-%m-%Y %H:%M"),
            "created_at": self._created_at.strftime("%d-%m-%Y %H:%M"),
            "updated_at": self._updated_at.strftime("%d-%m-%Y %H:%M"),
            "contributions": self._contributions,
            "accesses": self._accesses
        })
        
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
    def created_at(self) -> Optional[datetime]:
        return self._created_at
    
    @hybrid_property
    def updated_at(self) -> Optional[datetime]:
        return self._updated_at
    
    @hybrid_property
    def contributions(self) -> List[Contribution.__class__]:
        return self._contributions
    
    @hybrid_property
    def accesses(self) -> List[Access.__class__]:
        return self._accesses
        
    @hybrid_property
    def accesses_count(self) -> int:
        return len(self._accesses)
    

    

    

    
    
    