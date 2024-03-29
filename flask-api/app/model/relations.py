from datetime import datetime

from app.database import db

user_fk: str = "user.id"
song_fk: str = "song.id"

access = db.Table(
    "access",
    db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey(user_fk)),
    db.Column('song_id', db.Integer, db.ForeignKey(song_fk)),
    db.Column('created_at', db.DateTime, default=datetime.now)
    )

contribution = db.Table(
    "contribution",
    db.Model.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey(user_fk)),
    db.Column('song_id', db.Integer, db.ForeignKey(song_fk)),
    db.Column('created_at', db.DateTime, default=datetime.now),
    db.Column('lyrics', db.ARRAY(db.String), nullable=False)
    )

