#!/usr/bin/env python3

import json
import logging
import time

import redis
import requests

from config import API_SECRET, DASHBOARD_WORKER_API_BASE_URL

REFRESH_INTERVAL = 1  # seconds

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler("{0}/{1}.log".format("/var/log/ctf", "dashboard_worker"))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.INFO)


class RedisUpdater(object):
    def __init__(self):
        self.api_url = DASHBOARD_WORKER_API_BASE_URL
        self.params = {"secret": API_SECRET}
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.gameinfo = None
        self.teams_names = None
        self.services_names = None

    def helper(self):
        # Update information that is repeatedly used by ctf_* services
        url = '/'.join([self.api_url, "getgameinfo"])
        r = requests.get(url, params=self.params)
        self.gameinfo = r.json()
        teams_data = self.gameinfo["teams"]
        self.teams_names = {}
        for team_data in teams_data:
            self.teams_names[team_data["team_id"]] = team_data["team_name"]

        services_data = self.gameinfo["services"]
        self.services_names = {}
        for service_data in services_data:
            self.services_names[service_data["service_id"]] = service_data["service_name"]

    def ctf_services(self):

        url = '/'.join([self.api_url, "getlatestflagids"])
        r = requests.get(url, params=self.params)

        # print(r.json()["flag_ids"])

        # {'113': {'114': '545'}, '114': {'114': '546'}, '115': {'114': '543'}, '116': {'114': '544'}}
        #  team         srv     flag_id

        flag_ids = r.json()["flag_ids"]

        if len(flag_ids) == 0:
            logger.warning("No flag IDs found")

        if any(len(x) == 0 for x in flag_ids.values()):
            logger.warning("For at least one team the mapping from service to flag_id is empty: {}. This means the scorebot is not running or the game is not started yet or the scorebot has found services that are offline.".format(flag_ids))

        services = {}
        services_info = self.gameinfo['services']
        for service_info in services_info:
            service_id = service_info['service_id']

            if service_id not in services:
                services[service_id] = {}

            services[service_id]['description'] = service_info['description']
            services[service_id]['port'] = service_info['port']
            services[service_id]['name'] = service_info['service_name']
            services[service_id]['flag_id'] = \
                {
                    'description': service_info['flag_id_description'],
                    'flag_ids': [
                        {
                            'team_id': team_subnet_id,
                            'flag_id': flag_ids[team_subnet_id][str(service_id)],
                        } for team_subnet_id in
                        dict(list(filter(lambda kv: str(service_id) in kv[1], flag_ids.items())))
                    ]
                }

        self.store_redis('ctf_services', json.dumps(services))

    def ctf_services2(self):

        url = '/'.join([self.api_url, "getlatestflagids_multi"])
        r = requests.get(url, params=self.params)

        # print(r.json()["flag_ids"])

        # {'113': {'114': '545'}, '114': {'114': '546'}, '115': {'114': '543'}, '116': {'114': '544'}}
        #  team         srv     flag_id

        flag_ids = r.json()["flag_ids"]

        if len(flag_ids) == 0:
            logger.warning("No flag IDs found")

        if any(len(x) == 0 for x in flag_ids.values()):
            logger.warning("For at least one team the mapping from service to flag_id is empty: {}. This means the scorebot is not running or the game is not started yet or the scorebot has found services that are offline.".format(flag_ids))

        services = {}
        services_info = self.gameinfo['services']
        for service_info in services_info:
            service_id = service_info['service_id']

            if service_id not in services:
                services[service_id] = {}

            services[service_id]['description'] = service_info['description']
            services[service_id]['port'] = service_info['port']
            services[service_id]['name'] = service_info['service_name']
            services[service_id]['flag_id'] = \
                {
                    'description': service_info['flag_id_description'],
                    'flag_ids': [
                        {
                            'team_id': team_subnet_id,
                            'flag_id': flag_ids[team_subnet_id][str(service_id)],
                        } for team_subnet_id in
                        dict(list(filter(lambda kv: str(service_id) in kv[1], flag_ids.items())))
                    ]
                }

        self.store_redis('ctf_services2', json.dumps(services))

    def ctf_services_status(self):
        url = '/'.join([self.api_url, "getservicesstate"])
        r = requests.get(url, params=self.params)
        self.store_redis('ctf_services_status', json.dumps(r.json()["teams"]))

    def ctf_teams(self):
        teams_data = self.gameinfo["teams"]
        teams = {}
        for team_data in teams_data:
            team_id = int(team_data["team_id"])
            teams[team_id] = {"team_id": team_id,
                              "team_name": team_data["team_name"]}

        self.store_redis('ctf_teams', json.dumps(teams))

    def ctf_scores(self):
        url = '/'.join([self.api_url, "scores"])
        r = requests.get(url, params=self.params)
        scores_data = r.json()["scores"]
        scores = []
        for team in scores_data:
            team_id = int(team)
            scores.append(scores_data[team])
            scores[-1]["team_name"] = self.teams_names[team_id]

        scores.sort(key=lambda x: (x["score"], x['sla']), reverse=True)
        self.store_redis('ctf_scores', json.dumps(scores))

    def ctf_tick_change_time(self):
        url = '/'.join([self.api_url, "tick_duration"])
        r = requests.get(url, params=self.params)
        self.store_redis('ctf_tick_change_time', r.json())

    def ctf_jeopardy_list(self):
        url = '/'.join([self.api_url, "getjeopardylist"])
        r = requests.get(url, params=self.params)
        self.store_redis('ctf_jeopardy_list', json.dumps(r.json()))

    def store_redis(self, key, value):
        self.redis_client.set(key, value)

    def ctf_reasons(self):
        url = '/'.join([self.api_url, "reasons"])
        r = requests.get(url, params=self.params)
        # reasons_data = r.json()["reasons"]
        self.store_redis('ctf_reasons', json.dumps(r.json()))


def main():
    logger.info("Dashboard worker started")
    redis_updater = RedisUpdater()
    methods_to_run = [member for member in dir(redis_updater) if
                      member.startswith("ctf_") and '__func__' in
                      dir(getattr(redis_updater, member))]

    while True:
        redis_updater.helper()
        for method in methods_to_run:
            logger.debug("Refreshing %s" % (method))
            getattr(redis_updater, method)()

        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    main()
