import logging

import pymysql
from flask import Flask
from flask import render_template

from app.fakeapi import fakeapi
from app.api import api
from app.dashboard import dashboard
from db.database import db_session

pymysql.install_as_MySQLdb()

logging.basicConfig(level=logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

fileHandler = logging.FileHandler("{0}/{1}.log".format("/var/log", "dbapi"))
fileHandler.setFormatter(logFormatter)

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(dashboard)
app.register_blueprint(api, url_prefix='/api/v01')

app.register_blueprint(fakeapi, url_prefix='/fakeapi/v01')

app.logger.addHandler(fileHandler)
app.logger.setLevel(logging.DEBUG)  # ?

app.logger.error("Test")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404



from db.models import TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, \
    Tick, TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun

import flask_admin as admin
from flask_admin.contrib import sqla

from flask import request, Response
from werkzeug.exceptions import HTTPException


class ModelView(admin.contrib.sqla.ModelView):
    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response(
                "Please log in.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True


admin = admin.Admin(app, name='CTF-DB', template_mode='bootstrap3')
[admin.add_view(ModelView(m, db_session)) for m in [
    TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick,
    TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
]]

if __name__ == '__main__':
    app.run(debug=True)
