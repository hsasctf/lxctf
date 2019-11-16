from functools import wraps

from sqlalchemy import func

from flask_httpauth import HTTPBasicAuth

from flask import Blueprint, render_template, abort, request, jsonify, current_app
from flask import json
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g

from db.database import db_session
from db.models import TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, \
    Tick, TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
from app.api import verify_flag

from hashlib import sha512

import redis
import ipaddress

web = Blueprint('web', __name__,
                template_folder='templates')

auth = HTTPBasicAuth()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_team_num(ip):
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

def find_team(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        print("IP:"+ip)
        return f(*args, **kwargs)
    return decorated_function

def get_attacking_team():
    team = Team.query.filter(func.lower(Team.team_name) == func.lower(get_real_username(auth.username()))).first()
    event = Event.query.order_by(Event.id.desc()).first()
    attacking_team = AttendingTeam.query.filter_by(team=team, event=event).first()
    return attacking_team


@auth.get_password
def get_password(username):
    event = Event.query.order_by(Event.id.desc()).first()

    try_split = username.rsplit("-", 1)
    if len(try_split) == 2:
        if try_split[1] == "admin":
            real_username = try_split[0]
            team = Team.query.filter(func.lower(Team.team_name) == func.lower(real_username)).first()

            if AttendingTeam.query.filter_by(team=team, event=event).first():
                db_session.remove()
                return current_app.config["ADMIN_CREDENTIALS"][1]
            else:
                db_session.remove()
                return None
    team = Team.query.filter(func.lower(Team.team_name) == func.lower(username)).first()

    # only attending teams can login
    if not AttendingTeam.query.filter_by(team=team, event=event).first():
        return None

    db_session.remove()
    return team.password


@auth.hash_password
def hash_password(username, password):
    event = Event.query.order_by(Event.id.desc()).first()

    try_split = username.rsplit("-", 1)
    if len(try_split) == 2:
        if try_split[1] == "admin":
            real_username = try_split[0]
            team = Team.query.filter(func.lower(Team.team_name) == func.lower(real_username)).first()

            if AttendingTeam.query.filter_by(team=team, event=event).first():
                db_session.remove()
                return current_app.config["ADMIN_CREDENTIALS"][1]
            else:
                db_session.remove()
                return None

    team = Team.query.filter(func.lower(Team.team_name) == func.lower(username)).first()
    if not AttendingTeam.query.filter_by(team=team, event=event).first():
        return None

    db_session.remove()
    pw_salt = "{}{}".format(password, team.password_salt)
    return sha512(pw_salt.encode("utf8")).hexdigest()


def get_real_username(username):
    """allows admins to login as TEAMNAME-admin instead of TEAMNAME but with admin password"""
    try_split = username.rsplit("-", 1)
    if len(try_split) == 2:
        if try_split[1] == "admin":
            real_username = try_split[0]
            return real_username

    return username


@web.route("/")
@find_team
def index(team=None):
    return render_template('index.html')


@web.route('/config')
@find_team
def get_config(team=None):
    return jsonify({'ctf_name': current_app.config["CTF_NAME"], 'team_name': get_real_username(auth.username())})




@web.route('/flag', methods=['POST'])
@find_team
def submit_flag(team=None):
    attacking_team = get_attacking_team()

    return verify_flag(int(attacking_team.id), request.get_json()['flag'])


@web.route('/scores')
def get_scores():
    return redis_client.get('ctf_scores')


@web.route('/services')
@find_team
def get_services(team=None):
    return redis_client.get('ctf_services')


@web.route('/jeopardies')
@find_team
def get_jeopardies(team=None):
    return redis_client.get('ctf_jeopardy_list')


@web.route('/services_status')
@find_team
def get_services_status(team=None):
    status = json.loads(redis_client.get('ctf_services_status'))
    result = {}

    team = get_attacking_team()

    for state in status:
        if state['team_id'] == team.id:
            for entry in state['services']:
                result[entry['service_id']] = entry['state']

            break
    return jsonify(result)


@web.route('/tick_change_time')
def get_tick_duration():
    return redis_client.get('ctf_tick_change_time')
