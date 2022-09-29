import json
import time

from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db, Chord, User, Song
from better_profanity import profanity
from collections import defaultdict
import sshtunnel

app = Flask(__name__)
"""
tunnel = sshtunnel.SSHTunnelForwarder(
    ('sigma.tecnico.ulisboa.pt'), ssh_username='ist193584', ssh_password='C8*Bdaz2',
    remote_bind_address=('db.tecnico.ulisboa.pt', 5432)
)

tunnel.start()
"""
# IST DB
#db_str = "postgresql://ist193584:124jotPOC@127.0.0.1:{}/ist193584".format(tunnel.local_bind_port)
# RASPI DB
db_user = "postgres"
db_pw = "postgres"
db_host_ip = "192.168.1.206"
db_port = "5432"
db_name = "p06_canoa"
db_str = f"postgresql://{db_user}:{db_pw}@{db_host_ip}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

profanity.load_censor_words()
f = open("customBadWords.txt")
profanity.add_censor_words(f.readlines())
f.close()


@app.route('/')
def home():
#    result = Chord.query.all()
    return "Hello World"


@app.route('/signup', methods=['POST', 'GET'])
def form():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        scout_group = request.form['scout_group']
        password = request.form['password']
        if password != request.form['confirm_password']:
            return json.dumps({"result": "ERROR_PASSWORDS_NOT_MATCH"})
        if User.query.filter_by(email=email).first() != None:
            return json.dumps({"result": "ERROR_DUPLICATE_EMAIL"})
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            scout_group=scout_group)
        db.session.add(new_user)
        db.session.commit()
        return json.dumps({"result": "SUCCESS", "data": new_user.__repr__()})


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"

@app.route('/new_song', methods=['POST', 'GET'])
def new_song():
    if request.method == 'GET':
        return render_template('new_song_form.html')
    elif request.method == 'POST':
        title = request.form['title']
        if Song.query.filter_by(title=title).first() is not None:
            return "TITLE ALREADY IN USE"
        lyrics = request.form['lyrics']
        lyrics_list = lyrics.split('\r\n')
#        if check_profanity([title,lyrics]):
#            return json.dumps({"result": "ERROR: WATCH_YOUR_PROFANITY"})
        chords_list = {}
#        for i in range(len(lyrics_list)):
#            for j in range(len(lyrics_list[i])):
#                pos = "{};{}".format(i, j)
#                chords_list[pos] = None

        #categories = request.form['categories']
        #creator_id = request.form['creator_id']
        _new_song = Song(title=title,lyrics=lyrics_list,chords_list=json.dumps(chords_list),categories=[],creator_id=1001)
        db.session.add(_new_song)
        db.session.commit()
        return json.dumps({"result": "SUCCESS", "data": _new_song.__repr__()})


@app.route('/load_chords')
def load_chords():
    if len(Chord.query.all()) != 0:
        return "Chords already on db"
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
    return "Chords successfully loaded"


@app.route('/load_test_user', methods=['GET', 'POST'])
def load_test_user():
    if request.method == 'GET':
        return render_template('superuser_password_form.html')
    elif request.method == 'POST':
        if request.form['password'] == "123456":
            if User.query.filter_by(email="teste@teste").first() != None:
                return "SUPER USER ALREADY EXISTS"
            superuser = User(first_name="super",last_name="user",scout_group=1234,email="teste@teste",password="123456")
            db.session.add(superuser)
            db.session.commit()
            return "SUPER USER SUCCESSFULLY ADDED"
        return "WRONG PASSWORD"

@app.route('/api=get_available_songs', methods=['GET', 'POST'])
def get_available_songs():
    res = []
    if request.method == 'GET':
        songs = Song.query.all()
    elif request.method == 'POST':
        search = request.json["search"]
        songs = Song.query.filter(Song.title.contains(search)).all()

    for i in range(len(songs)):
        res.append(json.loads(songs[i].__repr__()))
    return json.dumps({"result": "SUCCESS", "data": res})


@app.route('/api=get_song_by_id', methods=['GET','POST'])
def get_song_by_id():
    if request.method == "POST":
        song_id = request.json['id']
        song = Song.query.filter_by(id=song_id).first()
        return json.dumps({"result": "SUCCESS", "data": song.__repr__()})


@app.route('/api=add_chord_to_song', methods=['GET','POST'])
def add_chord_to_song():
    if request.method == "GET":
        return render_template('add_chord_to_song.html')
    elif request.method == "POST":
        print("recebi")
        song_id = request.form['song_id']
        line = request.form['line']
        col = request.form['col']
        key = f"{line}:{col}"
        chord_id = request.form['chord_id']
        song = Song.query.filter_by(id=song_id).first()
        chords_list = json.loads(song.chords_list)
        print("chords list", chords_list)
        chords_list[key] = int(chord_id)
        song.chords_list = json.dumps(chords_list)
        db.session.commit()
        return json.dumps({"result": "SUCCESS", "data": song.__repr__()})

@app.route('/api=get_users', methods=['GET'])
def get_users():
    res = []
    users = User.query.all()
    for i in range(len(users)):
        tmp = {}
        id = users[i].id
        first_name = users[i].first_name
        last_name = users[i].last_name
        email = users[i].email
        tmp["id"] = id
        tmp["first_name"] = first_name
        tmp["last_name"] = last_name
        tmp["email"] = email
        res.append(tmp)
    return json.dumps({"result": "SUCCESS", "data": res})



def check_profanity(args):
    """
    Check if song title or song lyrics contains bad words
    :param title: title of the song
    :param lyrics: lyrics of the song
    :return: True if it contains any bad words
    """
    censor = False
    for text in args:
        if isinstance(text, list):
            for line in text:
                if profanity.contains_profanity(line):
                    censor = True
        elif isinstance(text, str):
            if profanity.contains_profanity(text):
                censor = True
        else:
            raise ValueError("not list nor text. type='{}'".format(text.__class__))
    return censor
"""
@app.route('/api=print_song_by_id', methods=['GET', 'POST'])
def print_song_by_id():
    if request.method == "GET":
        return render_template('print_song_by_id.html')
    elif request.method == "POST":
        song_id = request.form['id']
        song = Song.query.filter_by(id=song_id).first()
        chords = song.chords_list
        res = song.title
        for i in range(len(song.lyrics)):
    
    return json.dumps({"result": "SUCCESS", "data": song.__repr__()})
"""

if __name__ == '__main__':
    app.run(debug=True)