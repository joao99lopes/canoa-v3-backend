from datetime import datetime

from app.model import db, User, Song

user_fk: str = f"{User.__tablename__}"
song_fk: str = f"{Song.__tablename__}"

access = db.Table(
    "access",
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey(user_fk)),
    db.Column('song_id', db.Integer, db.ForeignKey(song_fk)),
    db.Column('created_at', db.Datetime, default=datetime.now)
    )

contribution = db.Table(
    "contribution",
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey(user_fk)),
    db.Column('song_id', db.Integer, db.ForeignKey(song_fk)),
    db.Column('created_at', db.Datetime, default=datetime.now),
    db.Column('lyrics', db.ARRAY(db.String), nullable=False)
    )

