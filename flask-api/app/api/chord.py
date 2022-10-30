from app.api import api_blueprint
from flask import jsonify
from app.database import db
from app.model.chord import Chord

PATH = '/chords'


@api_blueprint.route(f'{PATH}/', methods=['GET'])
def index():
    return jsonify(f"Hello World from {PATH}!"), 200


@api_blueprint.route(f'{PATH}/load', methods=['GET'])
def load_chords():
    if len(Chord.query.all()) != 0:
        return jsonify(msg="Chords already on db"), 403
    chords_list = [
        Chord(name='Do Maior', representation='C', is_minor=0),
        Chord(name='Do Sustenido Maior', representation='C#', is_minor=0),
        Chord(name='Re Maior', representation='D', is_minor=0),
        Chord(name='Re Sustenido Maior', representation='D#', is_minor=0),
        Chord(name='Mi Maior', representation='E', is_minor=0),
        Chord(name='Fa Maior', representation='F', is_minor=0),
        Chord(name='Fa Sustenido Maior', representation='F#', is_minor=0),
        Chord(name='Sol Maior', representation='G', is_minor=0),
        Chord(name='Sol Sustenido Maior', representation='G#', is_minor=0),
        Chord(name='La Maior', representation='A', is_minor=0),
        Chord(name='La Sustenido Maior', representation='A#', is_minor=0),
        Chord(name='Si Maior', representation='B', is_minor=0),
        Chord(name='Do Menor', representation='Cm', is_minor=1),
        Chord(name='Do Sustenido Menor', representation='C#m', is_minor=1),
        Chord(name='Re Menor', representation='Dm', is_minor=1),
        Chord(name='Re Sustenido Menor', representation='D#m', is_minor=1),
        Chord(name='Mi Menor', representation='Em', is_minor=1),
        Chord(name='Fa Menor', representation='Fm', is_minor=1),
        Chord(name='Fa Sustenido Menor', representation='F#m', is_minor=1),
        Chord(name='Sol Menor', representation='Gm', is_minor=1),
        Chord(name='Sol Sustenido Menor', representation='G#m', is_minor=1),
        Chord(name='La Menor', representation='Am', is_minor=1),
        Chord(name='La Sustenido Menor', representation='A#m', is_minor=1),
        Chord(name='Si Menor', representation='Bm', is_minor=1)
    ]

    for i in range(len(chords_list)):
        db.session.add(chords_list[i])
    db.session.commit()
    return jsonify(msg="Chords successfully loaded"), 200

