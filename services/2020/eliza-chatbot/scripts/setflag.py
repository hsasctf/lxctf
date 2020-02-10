#!/usr/bin/python2.7

# setflag script for ctf eliza-chatbot

# flag id: random string used as user in requests to logserver
# flag: random string used as single log entry

from __future__ import print_function

import requests
import urllib
import base64

from bs4 import BeautifulSoup
from random import choice
from string import ascii_lowercase
from contextlib import closing # needed for py2.7 httplib to be used with contextmanager


def _rand_str(length=10):
    return ''.join((choice(ascii_lowercase) for _ in range(length)))


def _flag():
    return 'FLAG_'+_rand_str(13)


class SetFlag():

    # POST flag as user flag_id, collect and return token
    def execute(self, ip, port, flag, token={}):
        assert isinstance(ip, str)
        assert isinstance(port, int) and (0 < port < 2**16)

        self.flag_id = _rand_str()
        self.error_msg = ''
        self.token = ''
        self.error = 0

        url = "http://" + str(ip) + ":" + str(port)

        session = requests.Session()

	cookies = token

        try:
            r_initial = session.get(url + '/', cookies=cookies)
        except (requests.ConnectionError, requests.RequestException, requests.HTTPError, requests.Timeout, requests.TooManyRedirects) as e:
            self.error = -1
            self.error_msg = str(e)
            return 0

        # all cookies from the server
        self.token = r_initial.cookies.get_dict()["hunchentoot-session"]

	print(self.token)

        setflag_value = "ID: " + str(self.flag_id) + " Flag: " + str(flag)
        data = base64.b64encode(setflag_value)

        r_get_message = session.get(url + '/?reply=' + data)

        if data == None:
            self.error = 1
            self.error_msg = "Base64 Encode-Error."

        else:
            self.error = 0

            r_set_message = session.get(url + '/?rebly=' + data)

    def result(self):
        return {'FLAG_ID': self.flag_id,
                'TOKEN': self.token,
                'ERROR': self.error,
                'ERROR_MSG': self.error_msg}


# debug
if __name__ == "__main__":

    ip = '127.0.0.1'
    port = 4242

    sf_obj = SetFlag()
    sf_obj.execute(ip, port, _flag())
    print(sf_obj.result())
