# IMPORTS
from flask import Flask, Blueprint, render_template, url_for, redirect
from secrets import token_hex
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

# SETUP
app = Flask(__name__)
app.secret_key = token_hex(16)
app.permanent_session_lifetime = timedelta(minutes=15)
db = SQLAlchemy(app)

# BLUEPRINTS
account = Blueprint('account', __name__)
app.register_blueprint(account, url_prefix='/account')

# MODELS
class Teacher(db.Model):
    pass

class Student(db.Model):
    pass

class Parent(db.Model):
    pass

class Scanner(db.Model):
    pass

class Scan(db.Model):
    pass

class Bus(db.Model):
    pass

class Driver(db.Model):
    pass

class Class(db.Model):
    pass

@app.route('/')
@app.route('/index')
def index():
    pass


@account.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

