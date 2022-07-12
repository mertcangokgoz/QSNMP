import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2855@localhost:5432/qsnmp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SESSION_COOKIE_NAME'] = "qsnmp_session"
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_KEY_PREFIX'] = "qsnmp_"

    db.init_app(app)
    return app
