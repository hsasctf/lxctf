from sqlalchemy import func

from flask_httpauth import HTTPBasicAuth

from flask import Blueprint, render_template, abort, request, jsonify, current_app
from flask import json
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g

from db.database import db_session
from db.models import TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, \
    Tick, TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun

from hashlib import sha512

import redis
import requests

web = Blueprint('web', __name__,
                template_folder='templates')

auth = HTTPBasicAuth()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


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
@auth.login_required
def index():
    return render_template('index.html')


@web.route('/config')
@auth.login_required
def get_config():
    return jsonify({'ctf_name': current_app.config["CTF_NAME"], 'team_name': get_real_username(auth.username())})


from app.api import verify_flag


@web.route('/flag', methods=['POST'])
@auth.login_required
def submit_flag():
    attacking_team = get_attacking_team()

    return verify_flag(int(attacking_team.id), request.get_json()['flag'])


@web.route('/scores')
def get_scores():
    return redis_client.get('ctf_scores')


@web.route('/services')
@auth.login_required
def get_services():
    return redis_client.get('ctf_services')


@web.route('/jeopardies')
@auth.login_required
def get_jeopardies():
    return redis_client.get('ctf_jeopardy_list')


@web.route('/services_status')
@auth.login_required
def get_services_status():
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


@web.route('/logout')
def logout():
    return ('Logout', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
