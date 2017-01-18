import os.path
import flask
import flask_login
from flask import session
from flask_restful import Api
from app.Model import User, HostName
from app.apiClass import MainAPI
from flask_sqlalchemy import SQLAlchemy

application = flask.Flask(__name__)
application.config.from_object(__name__)
application.jinja_env.autoescape = True | False

Api(application).add_resource(MainAPI, '/api/<int:id>/<oid>')

db = SQLAlchemy(application)

application.config.update(
    SECRET_KEY=os.urandom(32),
    SESSION_COOKIE_NAME="pre_demo",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_KEY_PREFIX="demo_",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:muratcan55@localhost:5432/demo-proje2'
)

login_manager = flask_login.LoginManager()
login_manager.init_app(application)
login_manager.session_protection = "strong"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@application.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html', error=e), 404


@application.route('/', methods=['GET'])
def main_page():
    if not session.get('logged_in'):
        return flask.redirect(flask.url_for('.login'))
    else:
        return flask.redirect(flask.url_for('.dashboard_panel'))


@application.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'GET':
        return flask.render_template('register.html')
    username = flask.request.form['username']
    email = flask.request.form['email']
    password = flask.request.form['password']
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    flask.flash('User successfully registered')
    return flask.redirect(flask.url_for('.login'))


@application.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')

    username = flask.request.form['login_username']
    password = flask.request.form['login_password']
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flask.flash('Username is invalid', 'error')
        return flask.redirect(flask.url_for('.login'))
    if not registered_user.check_password(password):
        flask.flash('Password is invalid', 'error')
        return flask.redirect(flask.url_for('.login'))
    flask_login.login_user(registered_user)
    flask.flash('Logged off successfully')
    return flask.redirect(flask.url_for('.dashboard_panel'))


@application.route('/Dashboard', methods=['GET'])
@flask_login.login_required
def dashboard_panel():
    return flask.render_template('panel.html')


@application.route('/delete/<int:id>/', methods=['GET'])
@flask_login.login_required
def delete_post_item(id):
    db.session.query(HostName).filter(HostName.id == id).delete()
    db.session.commit()
    return flask.redirect(flask.url_for('.ip_adr'))


@application.route('/Hostlist', methods=['GET', 'POST'])
@flask_login.login_required
def ip_adr():
    if flask.request.method == 'GET':
        fetchlist = HostName.query.all()
        return flask.render_template('ip.html', fetchlist=fetchlist)
    if flask.request.method == 'POST':
        host = HostName(flask.request.form['hostname'])
        db.session.add(host)
        db.session.commit()
        flask.flash('Host successfully Accepted')
        return flask.redirect(flask.url_for('.ip_adr'))


########################################
@application.route('/logout', methods=['GET'])
@flask_login.login_required
def logout():
    if session.get('logged_in') is False:
        return flask.redirect(flask.url_for('.main_page'))
    else:
        session['logged_in'] = False
        flask_login.logout_user()
        return flask.redirect(flask.url_for('.main_page'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return flask.render_template('blocked.html')


if __name__ == '__main__':
    application.run(host='127.0.0.1', debug=True)
