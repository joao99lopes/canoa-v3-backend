import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    scout_group = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Integer(), nullable=False)

    def __init__(self, first_name, last_name, scout_group, email, password, is_admin):
        self.first_name = first_name
        self.last_name = last_name
        self.scout_group = scout_group
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return json.dumps({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "scout_group": self.scout_group,
            "password": self.password,
            'is_admin': self.is_admin
        })


class Chord(db.Model):
    __tablename__ = "chord"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    representation = db.Column(db.String(), nullable=False)
    is_minor = db.Column(db.Integer(), nullable=False)
#    image = db.Column(db.Image)??????

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


class Song(db.Model):
    __tablename__ = "song"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    lyrics = db.Column(db.JSON(), nullable=False)
    chords_list = db.Column(db.JSON())
    categories = db.Column(db.JSON())
    creator_id = db.Column(db.Integer())
    is_verified = db.Column(db.Integer())

    def __init__(self,title,lyrics,chords_list,categories,creator_id):
        self.title = title
        self.lyrics = lyrics
        self.chords_list = chords_list
        self.categories = categories
        self.creator_id = creator_id
        self.is_verified = 0    # not verified by default

    def __repr__(self):
        return json.dumps({
            "title": self.title,
            "lyrics": self.lyrics,
            "chords_list": self.chords_list,
            "categories": self.categories,
            "creator_id": self.creator_id,
            "is_verified": self.is_verified
        })
