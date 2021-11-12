from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db, InfoModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@192.168.1.206:5432/p06_teste"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/signup')
def form():
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if confirm_password != password:
            return "Passwords did not match<br>Password: '{}'\n<br>Confirm password: '{}'".format(password,confirm_password)
        query_name = InfoModel.query.filter_by(name=name).first()
        query_email = InfoModel.query.filter_by(email=email).first()
        if query_email != None and query_name != None and query_email.email == email and query_name.name == name:
            return "Username '{}' and Email '{}' are already in use".format(name,email)
        elif query_email != None and query_email.email == email:
            return "Email '{}' is already in use".format(email)
        elif query_name != None and query_name.name == name:
            return "Username '{}' is already in use".format(name)
        new_user = InfoModel(name=name, age=age, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return f"Done!!"


if __name__ == '__main__':
    app.run(debug=True)