from flask import request, render_template, jsonify
from flask.blueprints import Blueprint
import json

from app.api import api_blueprint
from app.database import db
from app.model.song import Song

song_blueprint = Blueprint('song', __name__)
api_blueprint.register_blueprint(song_blueprint, url_prefix='/song')

@song_blueprint.route('/', methods=['GET'])
def index():
    return jsonify(f"Hello World from /song!"), 200


# TODO: check lyrics and title profanity
@song_blueprint.route('/new', methods=['POST'])
def add_new_song():
    try:
        if ("title" not in list(request.json.keys()))\
            or ("lyrics" not in list(request.json.keys())):
            return jsonify(error="Invalid input"), 406
        title = request.json['title']
        lyrics = request.json['lyrics']
        if Song.query.filter_by(title=title).first() is not None:
            return jsonify(error="Title already in use"), 406
        lyrics_list = lyrics.split('\r\n')
        song: Song = Song.query.filter_by(lyrics=lyrics_list).first()
        if song is not None:
            return jsonify(error=f"Song exists with title '{song.title}'"), 406
        new_song = Song(title=title,lyrics=lyrics_list,creator_id=1)
        db.session.add(new_song)
        db.session.commit()
        return jsonify(data=new_song.__repr__()), 200
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418
    
        
@song_blueprint.route('/get', methods=['GET'])
def get_songs():
    try:
        res = []
        songs : list = Song.query.all()
        for i in range(len(songs)):
            res.append(songs[i].__repr__())
        return jsonify(data=res), 200
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418
    
        
@song_blueprint.route('/get_by_id', methods=['GET'])
def get_song_by_id():
    try:
        if "id" in list(request.json.keys()):
            id = int(request.json["id"])
            res = Song.query.filter_by(id=id).first()
            if not res:
                return jsonify(error=f"No song with id {id}"), 406
            return jsonify(data=res.__repr__()), 200
        return jsonify(error="Invalid input"), 406
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418


@song_blueprint.route('/get_title_from_text', methods=['GET'])
def get_songs_with_title_match():
    try:
        res = []
        if "text" in list(request.json.keys()):
            text = str(request.json['text'])
            songs : list = Song.query.filter(Song.title.contains(text)).all()
            for i in range(len(songs)):
                res.append(songs[i].__repr__())
            return jsonify(data=res), 200
        else:
            return jsonify(error="Invalid input"), 406
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418
    
        
