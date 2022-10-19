import datetime
import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    is_verified = db.Column(db.Boolean(), default=False)
    verification_email_date = db.Column(db.Date(), nullable=False)
    playlists = db.Column(db.JSON(), nullable=False)

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password
        self.verification_email_date = datetime.datetime.now()
        self.playlists = {}

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            'is_admin': self.is_admin,
            'is_verified': self.is_verified,
            'verification_email_date': self.verification_email_date,
            "playlists": self.playlists
        })


class Chord(db.Model):
    __tablename__ = "chords"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    representation = db.Column(db.String(), nullable=False)
    is_minor = db.Column(db.Integer(), nullable=False)
#    image = db.Column(db.Image)??????  maybe url e depois saca a imagem a partir daí

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
    __tablename__ = "songs"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    lyrics = db.Column(db.ARRAY(db.String()), nullable=False)
    chords_list = db.Column(db.JSON(), nullable=False)
    categories = db.Column(db.ARRAY(db.String()), nullable=False)
    creator_id = db.Column(db.Integer(), nullable=False)
    is_verified = db.Column(db.Boolean(), default=False, nullable=False)
    created_at = db.Column(db.Date(), nullable=False)
    updated_at = db.Column(db.Date(), nullable=False)
    contributors = db.Column(db.JSON(), nullable=False)
    number_of_accesses = db.Column(db.Integer(), default=0, nullable=False)

    def __init__(self,title,lyrics,chords_list,categories,creator_id):
        self.title = title
        self.lyrics = lyrics
        self.chords_list = chords_list
        self.categories = categories
        self.creator_id = creator_id
        self.is_verified = False    # not verified by default
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.contributors = {}
        self.number_of_accesses = 0

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "title": self.title,
            "lyrics": self.lyrics,
            "chords_list": self.chords_list,
            "categories": self.categories,
            "creator_id": self.creator_id,
            "is_verified": self.is_verified,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "contributors": self.contributors,
            "number_of_accesses": self.number_of_accesses
        })
