import flask
import flask_login
from flask import session
from flask_restful import Api
from flask_restful import Resource
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

from app import create_app, db
from model import User, HostName

application = create_app()

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


class MainAPI(Resource):
    def get(self, id, oid):
        try:
            u = HostName.query.filter_by(id=id).first()
            session = getCmd(
                SnmpEngine(),
                CommunityData('public'),
                UdpTransportTarget((u.hostname, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
            errorIndication, errorStatus, errorIndex, varBinds = next(session)
            if errorIndication:
                return flask.flash('Error: %s' % errorIndication)
            elif errorStatus:
                return flask.flash(
                    '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1] or '?')
                )
            else:
                for varBind in varBinds:  # SNMP response contents
                    print(' = '.join([x.prettyPrint() for x in varBind]))
        except (TimeoutError, NameError, ReferenceError):
            return flask.flash('timed out while connecting to remote host')


# API class for the main page
Api(application).add_resource(MainAPI, '/api/<int:id>/<oid>')

if __name__ == '__main__':
    application.run(host='127.0.0.1', port=8080, debug=True)  # run app in debug mode on port 8080
