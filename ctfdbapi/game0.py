#!/usr/bin/env python3

import base64

from datetime import datetime, timedelta
import json

import sys

from db.database import db_session
from db.models import AttendingTeam, Event, Team, Submission, Flag, Challenge, Member, User, Catering, Food, Tick, TeamScriptsRunStatus, Script, ScriptPayload, ScriptRun


SERVICES_PATH = "../services/2019/"

import os


def read_service_script(path):
    with open(path) as script_file:
        return base64.b64encode(script_file.read().encode('utf8')).decode('utf8')

def create_challenge(name, port, authors, description, flag_id_description, points):

    # get newest event
    event = Event.query.order_by(Event.id.desc()).first()

    c = Challenge()
    c.name, c.port, c.authors, c.description, c.flag_id_description, c.event, c.points, c.type\
        = name, port, authors, description, flag_id_description, event, points, "ad"
    db_session.add(c)
    db_session.commit()
    return c

def create_script(challenge, type, payload):
    """
    only gets called if is_working is 1
    :param challenge:
    :param type:
    :param script:
    :return:
    """

    # get newest event
    event = Event.query.order_by(Event.id.desc()).first()

    s = Script()
    s.name = type + ".py"
    s.is_working = 1
    s.challenge = challenge
    s.type = type
    s.event = event


    db_session.add(s)
    db_session.commit()
    sp = ScriptPayload()
    sp.script = s
    sp.payload = payload.encode('utf8')
    db_session.add(sp)
    db_session.commit()





def combine_service_infos():
    project_dir = os.getcwd()
    os.chdir(SERVICES_PATH)
    infos = []

    for service in [x for x in os.listdir('.') if os.path.isdir(x)]:
        if service == "__init__.py":
            continue
        before_change = os.getcwd()
        os.chdir(service)

        print('Creating service {}'.format(str(service)))
        with open("info.json") as jsonfile:
            info = json.load(jsonfile)
            info['getflag'] = read_service_script(info['getflag'])
            info['setflag'] = read_service_script(info['setflag'])
            try:
                info['benign'] = [read_service_script(b) for b in info['benign']]
            except:
                pass
            infos.append(info)
        os.chdir(before_change)

    os.chdir(project_dir)
    with open('combined_info.json', 'w') as f:
        # infos = [1,2,3]
        json.dump(infos, f, ensure_ascii=False)




def create_all_services_and_scripts():
    with open("combined_info.json") as f:
        services_info = json.load(f)
        for service_info in list(services_info):
            try:
                if service_info['is_working'] == 1:
                    authors_string = ""

                    if 'authors' in service_info:
                        authors_string = ", ".join(service_info['authors'])
                    description = service_info.get('service_description', "")
                    flag_id_description = service_info.get('flag_id_description', "")
                    challenge = create_challenge(service_info['name'], service_info['port'], authors_string, description,
                                                flag_id_description, service_info['points'])


                    create_script(challenge, 'getflag', service_info['getflag'])
                    create_script(challenge, 'setflag', service_info['setflag'])
                    try:
                        for benign in service_info['benign']:
                            create_script(challenge, 'benign', benign)
                    except Exception as e:
                        print("Skipping benign script for challenge {}: {}".format(service_info['name'], str(e)))

                    print("imported", service_info['name'])
            except ValueError as e:
                print("service dir has wrong info.json" + str(e))




if __name__ == '__main__':

    event_added = input("Are the new event + attending teams already added to database? (yes/no): ")
    if event_added != "yes":
        print("Add event first before you run this script")
        exit(1)

    combine_service_infos()
    create_all_services_and_scripts()




