"""
This API is meant for dashboard_worker only.
Other IDs than in database are used
"""

from flask import Blueprint, render_template, abort, request, jsonify
from flask import json
from sqlalchemy import desc

from db.database import db_session
from db.models import AttendingTeam, Event, Challenge, Tick, \
    TeamServiceState, TeamScore, Flag

fakeapi = Blueprint('fakeapi', __name__,
                template_folder='templates')

from config import API_SECRET
from utils import get_current_tick
from sqlalchemy.sql import func, label



def get_service_state_by_tick(tick):
    if tick is None:
        return {"teams": []}
    tick_start_time = tick.created
    tick_end_time = tick.time_to_change
    event = Event.query.order_by(Event.id.desc()).first()

    teams = []

    for ateam in AttendingTeam.query.filter_by(event=event):
        services = []
        for service in Challenge.query.filter_by(type="ad", event=event):

            service_status = -1

            tss_list = TeamServiceState.query.filter(
                TeamServiceState.attending_team == ateam,
                TeamServiceState.challenge == service,
                TeamServiceState.created > tick_start_time,
                TeamServiceState.created < tick_end_time,
            )
            service_statuses = [tss.state for tss in tss_list]

            if len(service_statuses) != 0:
                service_status = min(service_statuses)

            services.append({'service_id': service.port, 'state': service_status})
        teams.append({'team_id': ateam.subnet, 'services': services})

    return {'teams': teams}


@fakeapi.route('/getgameinfo')
def get_game_info():
    if request.args.get('secret') != API_SECRET:
        abort(401)

    # current_tick, time_left = get_current_tick()
    # teams = get_service_state_by_tick(current_tick)
    #
    # return jsonify(get_service_state_by_tick(current_tick))

    event = Event.query.order_by(Event.id.desc()).first()

    ateams = AttendingTeam.query.filter_by(event=event).all()

    services = Challenge.query.filter_by(event=event, type='ad').all()  # TODO type jeopardy?

    return jsonify({
        "services": [
            {
                "service_id": s.port,
                "service_name": s.name,
                "port": s.port,
                "flag_id_description": s.flag_id_description,
                "description": s.description,
            } for s in services
        ],
        "teams": [
            {
                "team_id": at.subnet,
                "team_name": at.team.team_name,
                "ip_range": "10.40.{}".format(at.subnet)
            } for at in ateams
        ]
    })


@fakeapi.route("/getlatestflagids")
def get_latest_flag_ids():
    if request.args.get('secret') != API_SECRET:
        abort(401)

    flag_ids = {}

    event = Event.query.order_by(Event.id.desc()).first()

    ateams = AttendingTeam.query.filter_by(event=event)

    for ateam in ateams:
        services = AttendingTeam.query.filter_by(event=event)

        flag_ids[int(ateam.subnet)] = {}
        for service in Challenge.query.filter_by(type="ad", event=event):

            flag = Flag.query.filter_by(attending_team=ateam, challenge=service).order_by(Flag.created.desc()).first()
            if flag and flag.flag_id:
                flag_ids[int(ateam.subnet)][int(service.port)] = flag.flag_id

    to_return = {'flag_ids': flag_ids}
    return jsonify(to_return)


@fakeapi.route("/reasons")
def get_reasons():
    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()
    particiant_ids = [x.id for x in event.participants]


    result = [{"reason": "test"}]

    for team_score in TeamScore.query.filter(TeamScore.attending_team.has(AttendingTeam.id.in_(particiant_ids))):
        result.append({"reason": str(team_score.reason)})
        #print(str(result))
        break


    return jsonify(result)

@fakeapi.route('/getjeopardylist')
def get_jeopardy_list():
    if request.args.get('secret') != API_SECRET:
        abort(401)

    # get newest event:
    event = Event.query.order_by(Event.id.desc()).first()

    # get all jeopardies from this event
    jeos = Challenge.query.filter_by(type="jeopardy", event=event)

    # do not serialize the flags:
    public_jeos = [
        {
            "id": j.id,
            "name": j.name,
            "points": j.points,
            "port": j.port,
            "description": j.description.replace("\n", "<br>")

        } for j in jeos
    ]
    return jsonify(public_jeos)





@fakeapi.route("/tick_duration")
def get_tick_duration():
    _, seconds_to_next_tick = get_current_tick()
    return json.dumps(seconds_to_next_tick)


@fakeapi.route("/getservicesstate/<tick_id>")
def get_service_state_tick(tick_id):
    if request.args.get('secret') != API_SECRET:
        abort(401)

    tick = Tick.query.filter_by(id=tick_id).first()

    return jsonify(get_service_state_by_tick(tick))


@fakeapi.route("/getservicesstate")
def get_services_state():
    if request.args.get('secret') != API_SECRET:
        abort(401)

    current_tick, time_left = get_current_tick()

    return jsonify(get_service_state_by_tick(current_tick))



def get_uptime_for_team(ateam):
    event = Event.query.order_by(Event.id.desc()).first()

    # get all tss from a team grouped by services

    tsss1 = db_session.query(
        label('count', func.count(TeamServiceState.id)),
        TeamServiceState.challenge_id,
    ).group_by(TeamServiceState.challenge_id,
               ).filter_by(attending_team=ateam)

    total_counts = {}
    for tss in tsss1:
        total_counts[tss[1]] = tss[0]

    # get all tss from a team with state 2 where service is up grouped by service

    tsss2 = db_session.query(
        label('count', func.count(TeamServiceState.id)),
        TeamServiceState.challenge_id,
    ).group_by(TeamServiceState.challenge_id,
               ).filter_by(attending_team=ateam, state=2)

    up_counts = {}
    for tss in tsss2:
        up_counts[tss[1]] = tss[0]
    uptimes = {}
    for service_id in total_counts.keys():
        total = total_counts[service_id]
        up = 0
        try:
            up = up_counts[service_id]
        except:
            pass
        uptime = ((up * 1.0) / (total * 1.0)) * 100

        uptimes[service_id] = uptime

    # now average all the uptimes

    total = 0
    for service_id in uptimes.keys():
        total += uptimes[service_id]

    if len(uptimes) == 0:
        return 0
    return total / len(uptimes)



@fakeapi.route("/scores")
def scores():
    if request.args.get('secret') != API_SECRET:
        abort(401)

    event = Event.query.order_by(Event.id.desc()).first()
    particiant_ids = [x.id for x in event.participants]

    team_scores = db_session.query(TeamScore.attending_team_id,
                                   label('score', func.sum(TeamScore.score)),
                                   ).filter(TeamScore.attending_team_id.in_(particiant_ids)).group_by(
        TeamScore.attending_team_id).order_by(desc(func.sum(TeamScore.score))).all()

    return jsonify({'scores': {
       AttendingTeam.query.get(aid).subnet:  {
           'raw_score': int(raw_score),
           # only calculate SLA once per team in this dict comprehension:
           **(lambda sla: {'sla': sla, 'score': int(raw_score) * (float(sla) / 100.0)})(int(get_uptime_for_team(AttendingTeam.query.get(aid)))),
           'subnet': AttendingTeam.query.get(aid).subnet
       } for aid, raw_score, *args in team_scores
    }})
