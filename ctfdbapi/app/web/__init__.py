from functools import wraps

from sqlalchemy import func


from flask import Blueprint, render_template, abort, request, jsonify, current_app
from flask import json
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g

from db.database import db_session
from db.models import TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, \
    Tick, TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
from app.api import verify_flag

from hashlib import sha512

import redis

web = Blueprint('web', __name__,
                template_folder='templates')

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_team_num(ip):
    request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

def find_team(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        try:
            a, b, c, d = [int(x) for x in ip.split(".")]
            assert a == 10
            assert b in [40, 41, 42, 43]
            event = Event.query.order_by(Event.id.desc()).first()
            ateam = AttendingTeam.query.filter_by(subnet=c, event=event).one_or_none()
            team = ateam.team if ateam is not None else None
            if not team:
                return redirect(url_for('web.error'))
            kwargs['team'] = team
            kwargs['ateam'] = ateam
        except Exception as e:
            return redirect(url_for('error'))
        return f(*args, **kwargs)
    return decorated_function


@web.route("/error")
def error():
    return "ERROR, are you connected to VPN or are in the correct subnet?"



@web.route("/")
@find_team
def index(team=None, ateam=None):
    return render_template('index.html')


@web.route('/config')
@find_team
def get_config(team=None, ateam=None):
    team_name = "UNKNOWN"
    try:
        team_name = team.team_name
    except AttributeError:
        pass
    finally:
        return jsonify({'ctf_name': current_app.config["CTF_NAME"], 'team_name': team_name})




@web.route('/flag', methods=['POST'])
@find_team
def submit_flag(team=None, ateam=None):
    attacking_team = ateam

    return verify_flag(int(attacking_team.id), request.get_json()['flag'])


@web.route('/scores')
def get_scores():
    return redis_client.get('ctf_scores')


@web.route('/services')
@find_team
def get_services(team=None, ateam=None):
    return redis_client.get('ctf_services')


@web.route('/jeopardies')
@find_team
def get_jeopardies(team=None, ateam=None):
    return redis_client.get('ctf_jeopardy_list')


@web.route('/services_status')
@find_team
def get_services_status(team=None, ateam=None):
    status = json.loads(redis_client.get('ctf_services_status'))
    result = {}


    for state in status:
        if state['team_id'] == ateam.id:
            for entry in state['services']:
                result[entry['service_id']] = entry['state']

            break
    return jsonify(result)


@web.route('/tick_change_time')
def get_tick_duration():
    return redis_client.get('ctf_tick_change_time')
