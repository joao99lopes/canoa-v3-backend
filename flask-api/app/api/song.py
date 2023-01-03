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
        # check invalid input
        if ("title" not in list(request.json.keys())) \
                or ("lyrics" not in list(request.json.keys())):
            return jsonify(error="Invalid input"), 406

        title = request.json['title']
        lyrics = request.json['lyrics']
        # check if there's a song with the given title
        if Song.query.filter_by(title=title).first() is not None:
            return jsonify(error="Title already in use"), 406
        lyrics_list = lyrics.split('\n')
        # check if there's a song with the same lyrics
        song: Song = Song.query.filter_by(lyrics=lyrics_list).first()
        if song is not None:
            return jsonify(error=f"Song exists with title '{song.title}'"), 406

        # add new song
        new_song = Song(title=title, lyrics=lyrics_list, creator_id=1)
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
        songs: list = Song.query.all()
        for i in range(len(songs)):
            res.append(songs[i].__repr__())
        return jsonify(data=res), 200
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418


@song_blueprint.route('/get_by_id', methods=['GET'])
def get_song_by_id():
    try:
        if "id" in list(request.args.keys()):
            song_id = int(request.args["id"])
            res = Song.query.filter_by(id=song_id).first()
            if not res:
                return jsonify(error=f"No song with id {song_id}"), 406
            return jsonify(data=res.__repr__()), 200
        return jsonify(error="Invalid input"), 406
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418


@song_blueprint.route('/get_songs_with_title_match', methods=['GET'])
def get_songs_with_title_match():
    try:
        res = []
        test = request.args
        print(list(test.keys()))
        if "text" in list(request.args.keys()):
            text = str(request.args['text'])
            songs: list = Song.query.filter(Song.title.contains(text)).all()
            for i in range(len(songs)):
                res.append(songs[i].__repr__())
            return jsonify(data=res), 200
        else:
            return jsonify(error="Invalid input"), 406
    except Exception as e:
        print(e)
        return jsonify(error="Server error"), 418
