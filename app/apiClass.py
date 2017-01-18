import flask
from easysnmp import Session
from app.Model import HostName
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

application = flask.Flask(__name__)
db = SQLAlchemy(application)

application.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


class MainAPI(Resource):
    def get(self, id, oid):
        try:
            u = HostName.query.filter_by(id=id).first()
            session = Session(hostname=u.hostname, community='public', version=2, timeout=1, retries=3)
            oid = {'value': oid}
            result = {}
            for k in oid:
                result[k] = session.get(oid[k]).value
            return result
        except (TimeoutError, NameError, ReferenceError):
            return flask.flash('timed out while connecting to remote host')
