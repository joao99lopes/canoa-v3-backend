import json

from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db, Chord, User, Song
from better_profanity import profanity
import sshtunnel

app = Flask(__name__)

tunnel = sshtunnel.SSHTunnelForwarder(
    ('sigma.tecnico.ulisboa.pt'), ssh_username='ist193584', ssh_password='C8*Bdaz2',
    remote_bind_address=('db.tecnico.ulisboa.pt', 5432)
)

tunnel.start()

# IST DB
#db_str = "postgresql://ist193584:124jotPOC@127.0.0.1:{}/ist193584".format(tunnel.local_bind_port)
# RASPI DB
db_str = "postgresql://postgres:postgres@192.168.1.206:5432/p06_canoa"


app.config['SQLALCHEMY_DATABASE_URI'] = db_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

profanity.load_censor_words()
f = open("customBadWords.txt")
profanity.add_censor_words(f.readlines())
f.close()


@app.route('/')
def home():
    result = Chord.query.all()
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
        if User.query.filter_by(email=email).first() != None:
            return json.dumps({"result": "ERROR_DUPLICATE_EMAIL"})
        new_user = User(first_name=first_name,last_name=last_name, email=email, password=password, scout_group=scout_group)
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
        lyrics = request.form['lyrics']
        lyrics_list = lyrics.split('\n')
        if check_profanity([title,lyrics]):
            return json.dumps({"result": "ERROR: WATCH_YOUR_PROFANITY"})
        chords_list = {}
        for i in range(len(lyrics_list)):
            for j in range(len(lyrics_list[i])):
                pos = "{};{}".format(i, j)
                chords_list[pos] = None

        #categories = request.form['categories']
        #creator_id = request.form['creator_id']
        new_song = Song(title=title,lyrics=json.dumps({'lyrics':lyrics_list}),chords_list=json.dumps(chords_list),categories=json.dumps({}),creator_id=1001)
        db.session.add(new_song)
        db.session.commit()
        return json.dumps({"result": "SUCCESS", "data": new_song.__repr__()})


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

@app.route('/api=get_available_songs', methods=['GET'])
def get_available_songs():
    res = {}
    songs = Song.query.all()
    for i in range(len(songs)):
        id = songs[i].id
        name = songs[i].title
        res[id] = name
    return json.dumps({"result": "SUCCESS", "data": res})


@app.route('/api=get_song_by_id', methods=['GET','POST'])
def get_song_by_id():
    if request.method == "GET":
        return render_template('get_song_by_id.html')
    elif request.method == "POST":
        song_id = request.form['id']
        song = Song.query.filter_by(id=song_id).first()
        return json.dumps({"result": "SUCCESS", "data": song.__repr__()})


@app.route('/api=add_chord_to_song', methods=['POST'])
def add_chord_to_song():
    song_id = request.form['song_id']
    line = request.form['line']
    col = request.form['col']
    song = Song.query.filter_by(id=song_id).first()
    pos = (line,col)
    if pos in song.chords_list:
        return json.dumps({"result": "ERROR: POSITION_ALREADY_IN_USE"})
    else:
        chord_list = dict(json.loads(song.chords_list))
        new_chords_list[pos] = chord_id
        song.chords_list = new_chords_list
        db.session.commit()
        return json.dumps({"result": "SUCCESS", "data": song.__repr__()})



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


if __name__ == '__main__':
    app.run(debug=True)