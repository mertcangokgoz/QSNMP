from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, create_app


class User(db.Model):
    """USER
    User database code
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    active = db.Column(db.Boolean(), default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class HostName(db.Model):
    """HostName
    Hostname database code
    """
    __tablename__ = "hostnames"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostname = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, hostname):
        self.hostname = hostname

    def __repr__(self):
        return '%r' % self.hostname


db.create_all(app=create_app())
