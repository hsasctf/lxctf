"""
this flask blueprint contains web function that are used by the scorebot
web functions for dashboard_worker are in the blueprint "fakeapi"
"""

import random
import string

from flask import Blueprint, render_template, abort, request, jsonify
from flask import json
from jinja2 import TemplateNotFound
from sqlalchemy import desc

from db.database import db_session
from db.models import AttendingTeam, Event, Submission, Flag, Challenge, Member, User, Catering, Food, Tick, \
    TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun, \
    TeamScore

api = Blueprint('api', __name__,
                template_folder='templates')

from config import API_SECRET
from utils import get_current_tick
from sqlalchemy import inspect
from sqlalchemy.sql import func, label


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


FLAG_POSSIBILITIES = string.ascii_uppercase + string.digits + string.ascii_lowercase


def generate_new_flag():
    new_flag = ''.join(random.choice(FLAG_POSSIBILITIES) for x in range(13))
    return "FLAG_{}".format(new_flag)


##### API functions #####



@api.route("/getteamlist")
def get_team_list():
    """

    :return: {20: {"team_id": 20, "ip": "127.0.0.20"},
                    14: {"team_id": 14, "ip": "127.0.0.14"}, }
    """

    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()

    ateams = AttendingTeam.query.filter_by(event=event)

    res = {}

    for ateam in ateams:
        res[ateam.id] = {"team_id": ateam.id, "ip": "10.40.{}.1".format(ateam.subnet)}

    return jsonify(res)


##### iCTF section #######


@api.route('/state')
def current_state():
    """
    state_id is
    :return:
    """

    if request.args.get('secret') != API_SECRET:
        abort(401)

    # from sqlalchemy.ext.serializer import loads, dumps

    event = Event.query.order_by(Event.id.desc()).first()
    current_tick, seconds_to_next_tick = get_current_tick()
    # is 0,1337 when there is no tick for current event yet
    # is None, 1337 ??

    if current_tick is None:
        print("Warning: There is no current tick. Game not started yet?")
        return jsonify({
            'state_id': 0,
            'state_expire': 1337,
            'game_id': 0,
        })

    result = {
        'state_id': current_tick.id,
        'state_expire': seconds_to_next_tick,
        'game_id': event.id,
        # 'services':  [object_as_dict(u) for u in ],
        # 'scripts': list(Script.query.filter_by(event=event)),
        # 'run_scripts': [{'team_id': tsrs.attending_team.id, 'run_list': json.loads(tsrs.json_list_of_scripts_to_run) } for tsrs in TeamScriptsRunStatus.query.filter_by(tick=current_tick)]
    }

    services = []
    for service in Challenge.query.filter_by(type="ad", event=event):
        services.append({
            'service_id': service.id,
            'service_name': service.name,  # ??? TODO
            # 'type': str(service.type), # NEW
            'port': service.port,
        })
    result['services'] = services

    scripts = []
    for script in Script.query.filter_by(event=event):
        scripts.append({
            'script_id': script.id,
            'is_bundle': 0,
            'type': str(script.type).split(".")[-1],
            'script_name': script.name,
            'service_id': script.challenge.id,
        })
    result['scripts'] = scripts

    run_scripts = []
    for run_script in TeamScriptsRunStatus.query.filter_by(tick=current_tick):
        run_scripts.append({
            'team_id': run_script.attending_team.id,
            'run_list': json.loads(run_script.json_list_of_scripts_to_run),
        })
    result['run_scripts'] = run_scripts

    return jsonify(result)




def get_service_state_by_tick(tick):
    if tick is None:
        return {"teams": []}
    tick_start_time = tick.created
    tick_end_time = tick.time_to_change
    event = Event.query.order_by(Event.id.desc()).first()

    teams = []

    for team in AttendingTeam.query.filter_by(event=event):
        services = []
        for service in Challenge.query.filter_by(type="ad", event=event):

            service_status = -1

            tss_list = TeamServiceState.query.filter(
                TeamServiceState.attending_team == team,
                TeamServiceState.challenge == service,
                TeamServiceState.created > tick_start_time,
                TeamServiceState.created < tick_end_time,
            )
            service_statuses = [tss.state for tss in tss_list]

            if len(service_statuses) != 0:
                service_status = min(service_statuses)

            services.append({'service_id': service.id, 'state': service_status})
        teams.append({'team_id': team.id, 'services': services})

    return {'teams': teams}


@api.route("/setservicestate/<team_id>/<service_id>", methods=['GET'])
def set_state(team_id, service_id):
    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()
    status = int(request.args.get('status'))
    team_id = int(team_id)
    service_id = int(service_id)

    reason = request.args.get('reason')

    if not status in [0, 1, 2]:
        abort(400)

    tss = TeamServiceState()
    tss.attending_team = AttendingTeam.query.filter_by(id=team_id, event=event).first()
    tss.challenge = Challenge.query.filter_by(id=service_id, type="ad", event=event).first()
    tss.state = status
    if len(reason) > 248:
        tss.reason = reason[:248] + "<cut>"
    else:
        tss.reason = reason
    db_session.add(tss)
    db_session.commit()

    return jsonify({"result": "great success"})


@api.route("/allscripts")
def all_scripts():
    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()
    scripts = Script.query.filter_by(event=event)
    result = {
        "scripts": [
            {
                "id": s.id,
                "type": str(s.type).split(".")[-1],
                "name": "ctf_team",
                "is_ours": int(True),
                "is_bundle": int(s.is_bundle),
                "feedback": None,
                "team_id": None,  # is None for own scripts
                "service_id": s.challenge.id,
                "is_working": s.is_working,  # TODO is in DB nullable?

            } for s in scripts
        ],
    }
    return jsonify(result)


@api.route("/script/<script_id>")
def get_script(script_id):
    if request.args.get('secret') != API_SECRET:
        abort(401)

    script = Script.query.filter_by(id=script_id).first()

    script_payload = ScriptPayload.query.filter_by(script=script).first()

    result = {
        'payload': script_payload.payload.decode("utf8"),
        'id': script.id,  # ???
        'type': str(script.type).split(".")[-1],
        'name': script.name,  # ???
        'is_ours': int(True),
        'is_bundle': int(script.is_bundle),
        'team_id': None,  # for exploits??
        'service_id': script.challenge.id,
        'is_working': script.is_working,
    }

    return jsonify(result)


@api.route("/ranscript/<script_id>")
def ran_script(script_id):
    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()

    defending_team = AttendingTeam.query.filter_by(id=request.args.get('team_id'), event=event).first()
    error = int(request.args.get('error'))
    error_msg = request.args.get('error_msg', None)

    script = Script.query.filter_by(id=script_id).first()

    if str(script.type).split(".")[-1] == "exploit":
        abort(500)
        return

    script_run = ScriptRun()
    script_run.script = script
    script_run.attending_team = defending_team
    script_run.error = error
    if len(error_msg) > 2040:
        script_run.error_msg = error_msg[:2040] + "<cut>"  # XXX
    else:
        script_run.error_msg = error_msg
    db_session.add(script_run)
    db_session.commit()

    return jsonify({"result": "great success"})


# flag stuff
@api.route("/newflag/<team_id>/<service_id>")
def create_new_flag(team_id, service_id):
    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()

    new_flag = generate_new_flag()

    flag = Flag()
    flag.attending_team = AttendingTeam.query.filter_by(id=team_id, event=event).first()
    flag.challenge = Challenge.query.filter_by(id=service_id, type="ad").first()
    flag.flag = new_flag
    db_session.add(flag)
    db_session.commit()

    return jsonify({'flag': flag.flag})


@api.route("/setcookieandflagid/<flag>")
def set_cookie_and_flag_id(flag):
    if request.args.get('secret') != API_SECRET:
        abort(401)

    cookie = request.args.get('cookie', None)
    flag_id = request.args.get('flag_id', None)

    event = Event.query.order_by(Event.id.desc()).first()

    flag = Flag.query.filter_by(flag=flag).first()
    if flag.attending_team.event != event:
        abort(500)  # Flag is not from the correct event
        return

    flag.flag_id = flag_id
    flag.cookie = cookie
    db_session.commit()

    return jsonify({"result": "great success"})


@api.route("/getlatestflagandcookie/<team_id>/<service_id>")
def get_latest_flag_and_cookie(team_id, service_id):
    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()

    flag = Flag.query.filter_by(
        attending_team=AttendingTeam.query.filter_by(id=team_id, event=event).first(),
        challenge=Challenge.query.filter_by(id=service_id).first()
    ).order_by(Flag.id.desc()).first()


    result = {
        'flag': flag.flag,
        'cookie': flag.cookie,
        'flag_id': flag.flag_id,
    }

    return jsonify(result)




def verify_flag(attacking_team_id, flag):

    if not flag:
        return jsonify({'result': 'incorrect', 'points': None})

    try:
        flag_obj = Flag.query.filter_by(flag=flag).first()
    except:
        flag_obj = None

    event = Event.query.order_by(Event.id.desc()).first()

    attacking_team = AttendingTeam.query.filter_by(id=attacking_team_id, event=event).first()

    if attacking_team is None:
        return jsonify({'result': 'teamnotfound'})

    # check if already submitted by this team
    already_submitted = Submission.query.filter_by(
        attending_team=attacking_team,
        flag=flag_obj,
    ).first()

    # already submitted ad flags have the flag attribute always set, jeopardy never has a corresponding flag object
    if already_submitted is not None and flag_obj is not None:
        return jsonify({'result': 'alreadysubmitted', 'points': None})

    # already submitted jeopardy flag, flag is always None
    s = Submission.query.filter_by(
        attending_team=attacking_team, submitted_string=flag, flag=None
    ).first()
    if s is not None:
        return jsonify({'result': 'already_solved_or_incorrect_flag', 'points': None})

    # Submission will be created for all flags except already submitted flags
    # including invalid flags....
    submission = Submission()
    submission.attending_team = attacking_team
    submission.flag = flag_obj  # None if no flag could be found in db
    submission.submitted_string = flag
    db_session.add(submission)
    db_session.commit()

    existing_flag_in_db = Flag.query.filter_by(flag=flag).first()

    # valid flag
    if existing_flag_in_db:
        # First check if the flag was created in the current event
        if existing_flag_in_db.challenge.event != event:
            to_return = {'result': 'incorrect', 'points': None}
        elif existing_flag_in_db.attending_team.event != event:
            to_return = {'result': 'incorrect', 'points': None}


        # check if the flag is one of the latest 3
        # Only valid 3 ticks

        elif existing_flag_in_db.attending_team == attacking_team:
            to_return = {'result': 'ownflag', 'points': None}
        else:
            latest_flags = Flag.query.filter_by(
                attending_team=existing_flag_in_db.attending_team,  # defending team
                challenge=existing_flag_in_db.challenge
            ).order_by(Flag.created.desc()).limit(3).all()

            # Flags are valid 3 ticks

            if existing_flag_in_db.id in list(map(lambda x: x.id, latest_flags)):
                # Success! Give this team some points!
                points = existing_flag_in_db.challenge.points

                message = "Team {} ({}) successfully captured active flag from service {} from team {} ({})".format(attacking_team.subnet,
                                                                                                               attacking_team.team.team_name,
                                                                                                                    existing_flag_in_db.challenge.name,
                                                                                                                    existing_flag_in_db.attending_team.subnet,
                                                                                                                    existing_flag_in_db.attending_team.team.team_name
                                                                                                               )

                ts = TeamScore()
                ts.attending_team = attacking_team  # TODO test
                ts.score = points
                if len(message) > 248:
                    ts.reason = message[:248] + "<cut>"
                else:
                    ts.reason = message

                db_session.add(ts)
                db_session.commit()

                to_return = {'result': 'correct', 'points': points}


            else:
                to_return = {'result': 'notactive', 'points': None}
    else:
        event = Event.query.order_by(Event.id.desc()).first()

        # test if it's a jeopardy flag

        c = Challenge.query.filter_by(event=event, jeopardy_flag=flag, type="jeopardy").first()
        if not c.jeopary_flag:
            return jsonify({'result': 'ctf_system_configuration_error', 'points': None})


        if c is not None:
            # Jeopardy Success! Give this team some points!
            points = c.points
            message = "Team {} () successfully captured jeopardy flag from challenge {}".format(attacking_team.subnet, attacking_team.team.team_name, c.name)

            ts = TeamScore()
            ts.attending_team = attacking_team
            ts.score = points
            ts.reason = message

            db_session.add(ts)
            db_session.commit()

            to_return = {'result': 'correct', 'points': points}
            return jsonify(to_return)

        # the flag is invalid
        to_return = {'result': 'incorrect', 'points': None}
    return jsonify(to_return)


@api.route("/submitflag/<attacking_team_id>/<flag>")
def submit_flag(attacking_team_id, flag):
    """
    :param attacking_team_id: id of attending team that submits the flag
    :param flag: newest flag for a ad service
    :return:
    """
    if request.args.get('secret') != API_SECRET:
        abort(401)

    return verify_flag(attacking_team_id, flag)