#!/usr/bin/env python3

import logging
import time

from datetime import datetime, timedelta
import os
import sys

from db.database import db_session
from db.models import AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick, \
    TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun
from reset_db1 import combine_service_infos, create_all_services_and_scripts

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler("{0}/{1}.log".format("/var/log/ctf", "demo"))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)


def delete_prev_demos():
    Event.query.filter_by(is_demo=1).delete()
    db_session.commit()


def new_demo_event(ad_start_minutes=5):
    event = Event()
    event.registration_start = datetime.now() - timedelta(days=14)
    event.registration_end = datetime.now() - timedelta(days=2)
    event.start = datetime.now()
    event.end = datetime.now() + timedelta(hours=12)
    event.attack_defense_start = datetime.now() + timedelta(minutes=ad_start_minutes)
    event.is_demo = 1
    db_session.add(event)
    db_session.commit()
    return event


def assign_teams(event):
    teams = list(Team.query.all())
    for i, t in enumerate(teams[:3], start=1):
        a = AttendingTeam()
        a.event = event
        a.team = t
        a.subnet = i
        db_session.add(a)
        db_session.commit()
        logger.info(">> Team '{}' with subnet {} (IP: 10.40.{}.1) attends Event".format(t.team_name, i, i))
        logger.info(
            ">>> Team '{}' should be given the OpenVPN config in roles/vpn/files/client-team{}.ovpn; file must be updated with the IP address to reach OpenVPN server".format(
                t.team_name, i))
        logger.info(
            ">>> Team '{}' should be given the SSH public key file roles/infrastructure_lxd/files/team_keys/team{}.pub".format(
                t.team_name, i))
        logger.info(
            ">>> Team '{}' should be given the SSH private key file roles/infrastructure_lxd/files/team_keys/team{}".format(
                t.team_name, i))
    return teams[:3]


def check_rc(name, rc):
    if rc != 0:
        logger.error("Error starting {}, try `tmux kill-session -t {}`".format(name, name))
        sys.exit(1)


def game_ad_running():
    event = Event.query.order_by(Event.id.desc()).first()
    db_session.remove()
    # session.expire_all() # XXX
    return event.attack_defense_start < datetime.now() < event.end


def stop_tmux_sessions():
    for s in ['scorebot', 'dashboard_worker', 'gamebot', 'ctfdbapi']:
        rc = os.system("tmux kill-session -t {}".format(s))
        if rc != 0:
            logger.error(
                "TMUX session {} not stopped correctly, probably because session does not exist (for error see line before)".format(
                    s))
        else:
            logger.info("TMUX session {} stopped".format(s))


if __name__ == "__main__":
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
        logger.info("CTF DEMO started, ctrl-c to at any point, logs are written to /var/log/ctf/")
        logger.info("Stop tmux sessions and delete previous demos?")
        input()
        stop_tmux_sessions()
        delete_prev_demos()
        Team.query.filter_by(team_name="test").delete()

        logger.info("Starting Dashboard, takes up to 3 minutes in background")
        rc = os.system(
            "tmux new -d -s ctfdbapi -- 'keep-one-running python3 /opt/ctfdbapi/tornado_file.py'  \; pipe-pane 'cat >> /var/log/ctf/tornado.log'")
        check_rc("ctfdbapi", rc)

        logger.info("Create Event?")
        input()
        event = new_demo_event(ad_start_minutes=minutes)
        logger.info("Event: Defense time started, AD will start at {} (UTC)".format(event.attack_defense_start))



        logger.info("Add test team 'test1' with password Password1234")
        input()
        test_team = Team()
        test_team.team_name = 'test1'
        test_team.password = '3e881d5529e4560a59104c87d8851644cdd6d67c0d74c5e9de58cc0944c030b3fe2d76aedf3aa98e8245ec5c6066cb5e070b679ebff3fbead761f551b6f327f4'
        test_team.password_salt = 'GdMnKywT0G4KJADjZ8KQiYt2QWNOkmNx9SREn2StqZMuecaWcGgnK1ANqFjLSXON2VszHm6eECTUqEa4PrCHdNNdlIJY8sz6FMjCQmNpVOd5E5IRzCriTYFdAGuGP3cY'
        db_session.add(test_team)
        db_session.commit()

        logger.info("Add test team 'test2' with password Password1234")
        input()
        test_team = Team()
        test_team.team_name = 'test2'
        test_team.password = '3e881d5529e4560a59104c87d8851644cdd6d67c0d74c5e9de58cc0944c030b3fe2d76aedf3aa98e8245ec5c6066cb5e070b679ebff3fbead761f551b6f327f4'
        test_team.password_salt = 'GdMnKywT0G4KJADjZ8KQiYt2QWNOkmNx9SREn2StqZMuecaWcGgnK1ANqFjLSXON2VszHm6eECTUqEa4PrCHdNNdlIJY8sz6FMjCQmNpVOd5E5IRzCriTYFdAGuGP3cY'
        db_session.add(test_team)
        db_session.commit()


        logger.info("Add test team 'test3' with password Password1234")
        input()
        test_team = Team()
        test_team.team_name = 'test3'
        test_team.password = '3e881d5529e4560a59104c87d8851644cdd6d67c0d74c5e9de58cc0944c030b3fe2d76aedf3aa98e8245ec5c6066cb5e070b679ebff3fbead761f551b6f327f4'
        test_team.password_salt = 'GdMnKywT0G4KJADjZ8KQiYt2QWNOkmNx9SREn2StqZMuecaWcGgnK1ANqFjLSXON2VszHm6eECTUqEa4PrCHdNNdlIJY8sz6FMjCQmNpVOd5E5IRzCriTYFdAGuGP3cY'
        db_session.add(test_team)
        db_session.commit()

        logger.info("Let 3 random teams attend?")
        input()
        teams = assign_teams(event)


        logger.info("Add services to DB?")
        input()
        combine_service_infos()
        create_all_services_and_scripts()

        logger.info("Now Login to dashboard (for teams) at http://10.38.1.1:5000")
        logger.info("(Login as a team using admin password -> user: TEAMNAME-admin pw: from ctfdbapi/config.py)")
        logger.info("Starting admin interface at http://10.38.1.1:4999/admin/")
        logger.info("Login using credentials in ctfdbapi/config.py")
        from config import ADMIN_CREDENTIALS
        from urllib.parse import quote

        logger.info("-----")
        logger.info(
            "or login as Admin using this URL: http://{}@10.38.1.1:4999/admin/".format(':'.join(ADMIN_CREDENTIALS)))
        logger.info("-----")
        logger.info("=====")
        for t in teams + [test_team, ]:
            turl = "http://{}@10.38.1.1:5000".format(
                quote(t.team_name + "-admin") + ":" + quote(ADMIN_CREDENTIALS[1]))
            logger.info("Login as {} (only for demo purpose) -> {}".format(t.team_name,
                                                                           turl
                                                                           ))
        logger.info("=====")

        logger.info("Start gamebot?")
        input()
        rc = os.system(
            "tmux new -d -s gamebot -- 'keep-one-running python3 /opt/ctfdbapi/gamebot.py'")
        check_rc("gamebot", rc)

        logger.info("Start dashboard_worker?")
        input()
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

        rc = os.system(
            "tmux new -d -s scorebot -- 'keep-one-running python /opt/scorebot/scorebot.py'")
        check_rc("scorebot", rc)

        logger.info("Scorebot started")

        logger.info("Type ctrl-c to stop all services/bots")

        while True:
            time.sleep(0.1)


    except KeyboardInterrupt:
        a = input("Stopping tmux sessions, type YES to stop: ")
        if a == "YES":
            stop_tmux_sessions()
            logger.info("Stopped!")
            sys.exit()
