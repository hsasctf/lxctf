from db.database import db_session
from db.models import AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick, \
    TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
import datetime

def get_current_tick():
    event = Event.query.order_by(Event.id.desc()).first()

    tick = Tick.query.filter_by(event=event).order_by(Tick.id.desc()).first()

    if tick:
        seconds_left = (tick.time_to_change - datetime.datetime.now()).total_seconds()
    else:
        # before game is started return the seconds until it starts
        seconds_left = (event.attack_defense_start - datetime.datetime.now()).total_seconds()

    return tick, max(seconds_left, 0)