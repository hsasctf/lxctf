from functools import wraps

from sqlalchemy import func


from flask import Blueprint, render_template, abort, request, jsonify, current_app
from flask import json
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g

from db.database import db_session
from db.models import TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, \
    Tick, TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
from app.api import verify_flag

from hashlib import sha512

import redis

dashboard = Blueprint('web', __name__,
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


@dashboard.route("/error")
def error():
    return "ERROR, no team found for this source ip address"



@dashboard.route("/")
@find_team
def index(team=None, ateam=None):
    return render_template('index.html')


@dashboard.route('/config')
@find_team
def get_config(team=None, ateam=None):
    team_name = "UNKNOWN"
    try:
        team_name = team.team_name
    except AttributeError:
        pass
    finally:
        return jsonify({'ctf_name': current_app.config["CTF_NAME"], 'team_name': team_name})




@dashboard.route('/flag', methods=['POST'])
@find_team
def submit_flag(team=None, ateam=None):
    attacking_team = ateam

    return verify_flag(int(attacking_team.id), request.get_json()['flag'])


@dashboard.route('/scores')
def get_scores():
    return redis_client.get('ctf_scores')


@dashboard.route('/services')
@find_team
def get_services(team=None, ateam=None):
    svc = json.loads(redis_client.get('ctf_services2'))

    filter_flag_ids = {} # port (int) -> flag_ids (list)

    for port_str, obj in svc.items():
        filter_flag_ids[port_str] = [x for x in obj['flag_id']['flag_ids'] if int(x['team_id']) != int(ateam.subnet)]

    for k, v in svc.items():
        v['flag_id']['flag_ids'] = filter_flag_ids[port_str]

    return jsonify(svc)


@dashboard.route('/jeopardies')
@find_team
def get_jeopardies(team=None, ateam=None):
    return redis_client.get('ctf_jeopardy_list')


@dashboard.route('/services_status')
@find_team
def get_services_status(team=None, ateam=None):
    status = json.loads(redis_client.get('ctf_services_status'))
    result = {}


    for state in status:
        if state['team_id'] == ateam.subnet:
            for entry in state['services']:
                result[entry['service_id']] = entry['state']

            break
    return jsonify(result)


@dashboard.route('/tick_change_time')
def get_tick_duration():
    return redis_client.get('ctf_tick_change_time')

@dashboard.route('/reasons')
def get_reason():
    return redis_client.get('ctf_reasons')