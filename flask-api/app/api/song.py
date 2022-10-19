from flask import request, render_template, jsonify
import json
from pydantic import BaseModel

from app.api import api_blueprint
from app.model import db, Song

@api_blueprint.route('/new_song', methods=['GET'])
def new_song_request():
    return render_template('new_song_form.html')


class NewReservationPost(BaseModel):
    title: str
    lyrics: str
    
    
    
# TODO: check lyrics and title profanity
@api_blueprint.route('/new_song', methods=['POST'])
def add_new_song():
    title = request.form['title']
    if Song.query.filter_by(title=title).first() is not None:
        return "TITLE ALREADY IN USE"
    lyrics = request.form['lyrics']
    lyrics_list = lyrics.split('\r\n')
    chords_list = {}
    new_song = Song(title=title,lyrics=lyrics_list,chords_list=json.dumps(chords_list),categories=[],creator_id=1001)
    db.session.add(new_song)
    db.session.commit()
    return jsonify(data=new_song), 200
