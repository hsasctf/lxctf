#!/usr/bin/env python3

import logging
import time

from datetime import datetime, timedelta
import os
import sys

from db.database import db_session
from db.models import AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick, \
    TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
from manage_add_services import combine_service_infos, create_all_services_and_scripts

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler("{0}/{1}.log".format("/var/log", "event"))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)


# löschen bereits vorhandenen Demos/Event
#def delete_prev_demos():
#    Event.query.filter_by(is_demo=1).delete()
#    db_session.commit()

# erstellen einer neuen Demo bzw. eines neuen Event
#def new_demo_event(ad_start_minutes=5):
#    event = Event()
    # festlegen von dem startdatum der Registration
#    event.registration_start = datetime.now() - timedelta(days=14) # + timedelta(days=13) stand 25.12
    # festlegen von dem enddatum der Registartion
#    event.registration_end = datetime.now() - timedelta(days=2) # + timedelta(days=20) stand 25.12 bis 14.01
    # Start des Events
#    event.start = datetime.now() # + timedelta(days=23) # 17.01
    # End des Events
#    event.end = datetime.now() + timedelta(hours=12) # + timedelta(days=23 hours=12)
#    event.attack_defense_start = datetime.now() + timedelta(minutes=ad_start_minutes)
    # setzt den demo wert auf 1 für spätere um es wieder zu löschen
#    event.is_demo = 1
#    db_session.add(event)
#    db_session.commit()
#    return event


#def assign_teams(event):
    # hier werden alle Team abgerufen und die subnet verteilt.
    # Es wird auch geschildert was dem Team zur Verfügung gestellt werden muss
#    teams = list(Team.query.all())
#    for i, t in enumerate(teams[:3], start=1):
#        a = AttendingTeam()
#        a.event = event
#        a.team = t
#        a.subnet = i
#        db_session.add(a)
#        db_session.commit()
#        logger.info(">> Team '{}' with subnet {} (IP: 10.40.{}.1) attends Event".format(t.team_name, i, i))
#        logger.info(
#            ">>> Team '{}' should be given the OpenVPN config in roles/vpn/files/client-team{}.ovpn; file must be updated with the IP address to reach OpenVPN server".format(
#                t.team_name, i))
#        logger.info(
#            ">>> Team '{}' should be given the SSH public key file roles/infrastructure_lxd/files/team_keys/team{}.pub".format(
#                t.team_name, i))
#        logger.info(
#            ">>> Team '{}' should be given the SSH private key file roles/infrastructure_lxd/files/team_keys/team{}".format(
#                t.team_name, i))
#    return teams[:3]


def check_rc(name, rc):
    # tmux(terminal emulator) schließt sessions
    if rc != 0:
        logger.error("Error starting {}, try `tmux kill-session -t {}`".format(name, name))
        sys.exit(1)

# Hier wird angegeben wann bzw. in was für einem Zeitraum das Event angegeben
def game_ad_running():
    event = Event.query.order_by(Event.id.desc()).first()
    db_session.remove()
    # session.expire_all() # XXX
    return event.attack_defense_start < datetime.now() < event.end


# Hier werden die emulatoren Sessions geschlossen für scorebot,dasboard_worker,gamebot,ctfdbapi
def stop_tmux_sessions():
    for s in ['scorebot', 'dashboard_worker', 'gamebot', 'ctfdbapi']:
        rc = os.system("tmux kill-session -t {}".format(s))
        if rc != 0:
            # Fehler meldung wenn etwas schief gelaufen ist
            logger.error(
                "TMUX session {} not stopped correctly, probably because session does not exist (for error see line before)".format(
                    s))
        else:
            logger.info("TMUX session {} stopped".format(s))


# python interpreter does two things
# it sets a few special variable like __name__
# it executes all of the code in the file
# if execute the file it assigns __main__ to __name__
# ab hier werden die ganzen funktionen aufgerufen die oben erstellt wurden

if __name__ == "__main__":
    # Hier haben wir die Angabe wie lang es dauert bis der AD startet
    # sys.argvis a list in Python which contains command-line arguments passed to the script
    if len(sys.argv) != 2:
        print("run: python3 {} <minutes until AD starts>".format(sys.argv[0]))
        sys.exit(1)
    try:
        minutes = int(sys.argv[1])
        assert minutes >= 0
    except ValueError:
        print("run: python3 {} <minutes until AD starts>".format(sys.argv[0]))
        sys.exit(1)
    except AssertionError:
        print("run: python3 {} <minutes until AD starts>".format(sys.argv[0]))
        sys.exit(1)

    try:
        # the logger.info ist lediglich eine Ausgabe für diagnose Zwecke
        logger.info("CTF DEMO started, ctrl-c to at any point, logs are written to /var/log/ctf/")
        logger.info("Stop tmux sessions and delete previous demos?")
        input()
        stop_tmux_sessions()
        delete_prev_demos()
        #Team.query.filter_by(team_name="test").delete()

        logger.info("Starting Dashboard, takes up to 3 minutes in background")
        # execute the command in a subshell
        rc = os.system(
            "tmux new -d -s ctfdbapi -- 'keep-one-running python3 /opt/ctfdbapi/tornado_file.py'  \; pipe-pane 'cat >> /var/log/ctf/tornado.log'")
        check_rc("ctfdbapi", rc)

        logger.info("Create Event?")
        input()
        event = new_demo_event(ad_start_minutes=minutes)
        logger.info("Event: Defense time started, AD will start at {} (UTC)".format(event.attack_defense_start))

        logger.info("Let all teams attend?")
        input()
        teams = assign_teams(event)

        # hier wird beschreiben was für Werte das team bekommt
        # logger.info("Add test team 'test' with password Password1234")
        # input()
        # test_team = Team()
        # test_team.team_name = 'test'
        # test_team.password = '3e881d5529e4560a59104c87d8851644cdd6d67c0d74c5e9de58cc0944c030b3fe2d76aedf3aa98e8245ec5c6066cb5e070b679ebff3fbead761f551b6f327f4'
        # test_team.password_salt = 'GdMnKywT0G4KJADjZ8KQiYt2QWNOkmNx9SREn2StqZMuecaWcGgnK1ANqFjLSXON2VszHm6eECTUqEa4PrCHdNNdlIJY8sz6FMjCQmNpVOd5E5IRzCriTYFdAGuGP3cY'
        # db_session.add(test_team)
        # db_session.commit()

        # atest_team = AttendingTeam()
        # atest_team.team = test_team
        # atest_team.event = event
        # atest_team.subnet = 4
        # db_session.add(atest_team)
        # db_session.commit()

        # Service einbinden
        logger.info("Add services to DB?")
        input()
        combine_service_infos()
        create_all_services_and_scripts()

        # Team interface
        logger.info("Now Login to dashboard (for teams) at http://10.38.1.1:5000")
        logger.info("(Login as a team using admin password -> user: TEAMNAME-admin pw: from ctfdbapi/config.py)")
        # Admin interface
        logger.info("Starting admin interface at http://10.38.1.1:4999/admin/")
        logger.info("Login using credentials in ctfdbapi/config.py")
        from config import ADMIN_CREDENTIALS
        from urllib.parse import quote

        logger.info("-----")
        logger.warning("Firefox recommended")
        logger.info(
            "or login as Admin using this URL: http://{}@10.38.1.1:4999/admin/".format(':'.join(ADMIN_CREDENTIALS)))
        logger.info("-----")
        logger.info("=====")
        for t in teams: # + [test_team, ]:
            turl = "http://{}@10.38.1.1:5000".format(
                quote(t.team_name + "-admin") + ":" + quote(ADMIN_CREDENTIALS[1]))
            logger.info("Login as {} (only for demo purpose) -> {}".format(t.team_name,
                                                                           turl
                                                                           ))
        logger.info("=====")

        logger.info("Start gamebot?")
        input()
        # starts gamebot
        rc = os.system(
            "tmux new -d -s gamebot -- 'keep-one-running python3 /opt/ctfdbapi/gamebot.py'")
        check_rc("gamebot", rc)

        logger.info("Start dashboard_worker?")
        input()
        # starts dashboard_worker
        rc = os.system(
            "tmux new -d -s dashboard_worker -- 'keep-one-running python3 /opt/ctfdbapi/dashboard_worker.py'")
        check_rc("dashboard_worker", rc)


        logger.info("Continue?")
        input()

        logger.info("Scorebot will start automatically at {} (UTC)".format(event.attack_defense_start))
        while True:
            time.sleep(1)
            if game_ad_running():
                break
        logger.info("AD started")
        logger.info("Starting scorebot")

        # starts scorebot
        rc = os.system(
            "tmux new -d -s scorebot -- 'keep-one-running python /opt/scorebot/scorebot.py'")
        check_rc("scorebot", rc)

        logger.info("Scorebot started")

        logger.info("Type ctrl-c to stop all services/bots")

        while True:
            time.sleep(0.1)


    except KeyboardInterrupt:
        # input to stop the sessions
        a = input("Stopping tmux sessions, type YES to stop: ")
        if a == "YES":
            stop_tmux_sessions()
            logger.info("Stopped!")
            sys.exit()
