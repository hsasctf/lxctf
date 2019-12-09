import contextlib
from datetime import datetime

from ctfdbapi.db.database import db_session


from ctfdbapi.datetime import datetime, timedelta
from ctfdbapi.db.models import AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun, \
    TeamScore, TeamServiceState


def add_test():
    tick = Tick()
    tick.time_to_change = datetime.now()

    print("Tick mit ID {} geaddet".format(tick.id))  # None

    db_session.add(tick)
    db_session.commit()

    print("Tick mit ID {} geaddet".format(tick.id))


def update_test():

    ut = Tick.query.all()[0]
    ut.time_to_change = datetime.now()
    db_session.add(ut)
    db_session.commit()

def test_before_start_and_ad(step_minutes=5):

    # Delete all existing Rows
    [model.query.delete() for model in [AttendingTeam, Event, Team, Submission, Flag, Challenge, Sla, Member, User, Catering, Food, Tick, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun]]
    db_session.commit()

    event = Event()
    event.registration_start = datetime.now() - timedelta(days=14)
    event.registration_end = datetime.now() - timedelta(days=2)
    event.start = datetime.now() + timedelta(minutes=step_minutes)
    event.end = datetime.now() + timedelta(days=3)
    event.attack_defense_start = datetime.now() + timedelta(minutes=step_minutes)
    db_session.add(event)
    db_session.commit()


    c1 = Challenge()
    c1.event = event
    c1.name = "Jeo1000"
    c1.points = 1000
    c1.type = 'jeopardy'
    db_session.add(c1)
    db_session.commit()

    c2 = Challenge()
    c2.event = event
    c2.name = "Ad5000"
    c2.points = 5000
    c2.type = 'ad'
    db_session.add(c2)
    db_session.commit()

    c3 = Challenge()
    c3.event = event
    c3.name = "Ad700"
    c3.points = 700
    c3.type = 'ad'
    db_session.add(c3)
    db_session.commit()


def jeopardy_and_teams(event):
    c1 = Challenge()
    c1.event = event
    c1.name = "Jeo1000"
    c1.description = ".."

    c1.points = 1000
    c1.type = 'jeopardy'
    db_session.add(c1)
    db_session.commit()

    c2 = Challenge()
    c2.event = event
    c2.name = "Jeo5000"
    c2.description = ".."
    c2.points = 5000
    c2.type = 'jeopardy'
    db_session.add(c2)
    db_session.commit()

    c3 = Challenge()
    c3.event = event
    c3.name = "Jeo700"
    c3.description = ".."
    c3.points = 700
    c3.type = 'jeopardy'
    db_session.add(c3)
    db_session.commit()

    for i in range(1,5):
        t = Team()
        t.team_name = "Team{}".format(i)
        t.password = "nix"
        t.password_salt = "nix"
        a = AttendingTeam()
        a.event = event
        a.team = t
        a.subnet = i
        db_session.add(t)
        db_session.add(a)
        db_session.commit()




def test_running_ad_game(until_end_minutes=60): # fixme correct time

    # Delete all existing Rows
    [model.query.delete() for model in [
        TeamScore, AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick,
        TeamServiceState, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
    ]]
    db_session.commit()

    event = Event()
    event.registration_start = datetime.now() - timedelta(days=14)
    event.registration_end = datetime.now() - timedelta(days=2)
    event.start = datetime.now() - timedelta(hours=1) # start patch time
    event.attack_defense_start = datetime.now() + timedelta(seconds=15)

    event.end = datetime.now() + timedelta(minutes=until_end_minutes)

    db_session.add(event)
    db_session.commit()


    jeopardy_and_teams(event)





if __name__ == '__main__':
    test_running_ad_game(30) # FIXME corrent time





