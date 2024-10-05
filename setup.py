# IMPORTS
from flask import Flask, session, request
from secrets import token_hex
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from mails import gmail


app = Flask(__name__)
app.secret_key = token_hex(16)
app.permanent_session_lifetime = timedelta(minutes=15)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
