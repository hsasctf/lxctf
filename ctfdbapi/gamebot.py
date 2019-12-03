#!/usr/bin/env python3


import json
import logging
import random
from datetime import datetime, timedelta
from time import sleep, time

from db.database import db_session
from db.models import AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Tick, \
    TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun

TICK_TIME_IN_SECONDS = 180  # SET TO 180

NUMBER_OF_BENIGN_SCRIPTS = 2
NUMBER_OF_GET_SET_FLAG_COMBOS = 1

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler("{0}/{1}.log".format("/var/log/ctf", "gamebot"))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.DEBUG)


def game_ad_running():
    event = Event.query.order_by(Event.id.desc()).first()
    db_session.remove()
    # session.expire_all() # XXX
    return event.attack_defense_start < datetime.now() < event.end


#
def main():
    event = Event.query.order_by(Event.id.desc()).first()
    while not game_ad_running():
        event = Event.query.order_by(Event.id.desc()).first()

        logger.info("AD Game is not running. Gamebot will start at {} (UTC) (System time (UTC) now is {})".format(
            str(event.attack_defense_start), str(datetime.now())))
        sleep(10)

    current_tick, seconds_left = get_current_tick()
    if current_tick != None:
        # Gibt schon einen Tick, dann erstelle nicht direkt noch einen
        logger.info("We must be picking up from the last run. Sleep for", seconds_left, "until the next tick.")
        sleep(seconds_left)

    while True:
        event = Event.query.order_by(Event.id.desc()).first()

        if not game_ad_running():
            logger.info("Gamed ended at {}".format(str(datetime.now())))
            break

        # Create a new tick
        time_to_sleep = random.uniform(TICK_TIME_IN_SECONDS - 30, TICK_TIME_IN_SECONDS + 30)

        tick = Tick()
        tick.time_to_change = datetime.now() + timedelta(seconds=time_to_sleep)
        tick.event = event
        db_session.add(tick)
        db_session.commit()
        # db_session.remove()

        num_benign_scripts = random.randint(max(1, NUMBER_OF_BENIGN_SCRIPTS - 1), NUMBER_OF_BENIGN_SCRIPTS + 1)

        # Decide what scripts to run against each team

        for attending_team in AttendingTeam.query.filter_by(event=event):
            list_of_scripts_to_execute = get_list_of_scripts_to_run(Challenge.query.filter_by(type='ad', event=event),
                                                                    num_benign_scripts)
            tsrs = TeamScriptsRunStatus()
            tsrs.attending_team = attending_team
            tsrs.tick = tick
            tsrs.json_list_of_scripts_to_run = json.dumps(list_of_scripts_to_execute, ensure_ascii=False)

            db_session.add(tsrs)
            db_session.commit()
        # db_session.remove()

        # Sleep for the amount of time until the next tick
        time_diff_to_sleep = tick.time_to_change - datetime.now()
        seconds_to_sleep = time_diff_to_sleep.seconds + (time_diff_to_sleep.microseconds / 1E6)

        if time_diff_to_sleep.total_seconds() < 0:
            logger.debug("Time left is negative: {}".format(time_diff_to_sleep))
            seconds_to_sleep = 0

        logger.info("Sleeping for {}".format(seconds_to_sleep))
        sleep(seconds_to_sleep)
        logger.info("Awake")


def get_list_of_scripts_to_run(challenges, num_benign_scripts):
    # we want to run all the set flags first, then a random mix of benign and get flags
    set_flag_scripts = []
    get_flag_scripts = []
    benign_scripts = []

    for challenge in challenges:
        results = Script.query.filter_by(challenge=challenge, is_working=True)
        logger.debug("Getting scripts for challenge {} --> {}".format(challenge, [r.__str__() for r in results]))

        benigns = []

        for result in results:
            type = str(result.type)
            if type == 'ScriptType.getflag':
                get_flag_scripts.append(result.id)
            elif type == 'ScriptType.setflag':
                set_flag_scripts.append(result.id)
            elif type == 'ScriptType.benign':
                benigns.append(result.id)
            elif type == 'ScriptType.exploit':
                assert False, "In this version, we should never be running exploits"

        for i in range(num_benign_scripts):
            if benigns:
                benign_script = random.choice(benigns)
                benign_scripts.append(benign_script)


    logger.debug("Benign Scripts: {}".format(benign_scripts))
    logger.debug("Getflag Scripts: {}".format(get_flag_scripts))
    logger.debug("Setflag Scripts: {}".format(set_flag_scripts))

    random.shuffle(set_flag_scripts)

    other_scripts = [*get_flag_scripts, *benign_scripts]  # combine lists
    random.shuffle(other_scripts)

    db_session.remove()

    return [*set_flag_scripts, *other_scripts]


def get_current_tick():
    event = Event.query.order_by(Event.id.desc()).first()

    tick = Tick.query.filter_by(event=event).order_by(Tick.id.desc()).first()

    seconds_left = 1337

    if tick:
        seconds_left = (tick.time_to_change - datetime.now()).total_seconds()
        if seconds_left < 0:
            seconds_left = 0

    db_session.remove()

    return tick, seconds_left


if __name__ == "__main__":
    # for c in Challenge.query.filter_by(type='ad'):
    #     print(c.name)
    logger.info("Gamebot started")

    import sys

    sys.exit(main())
