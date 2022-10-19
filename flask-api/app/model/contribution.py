from datetime import datetime

from app.model import db, User, Song

user_fk = f"{User.__tablename__}"
song_fk = f"{Song.__tablename__}"

class Contribution(db.Model):
    __tablename__ = "contribution"
    db.Column('user_id', db.Integer, db.ForeignKey(user_fk))
    db.Column('song_id', db.Integer, db.ForeignKey(song_fk))
    db.Column('created_at', db.Datetime, default=datetime.now)
    db.Column('lyrics', db.ARRAY(db.String), nullable=False)
    
