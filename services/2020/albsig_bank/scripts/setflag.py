#!/usr/bin/python2.7

from __future__ import print_function
import requests

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
    def execute(self, ip, port, flag):
        assert isinstance(ip, str)
        assert isinstance(port, int) and (0 < port < 2**16)

        self.flag_id = _rand_str()
        self.error_msg = ''
        self.token = ''
        self.error = 0

        url = "http://" + str(ip) + ":" + str(port)

        session = requests.Session()

        try:
            r_initial = session.get(url + '/login')
        except (requests.ConnectionError, requests.RequestException, requests.HTTPError, requests.Timeout, requests.TooManyRedirects) as e:
            self.error = -1
            self.error_msg = str(e)
            return

        csrf_soup = BeautifulSoup(r_initial.content)
        csrf_token = csrf_soup.find('input', {'name':'csrf_token'})['value']

        data = {'csrf_token':csrf_token,
            'email':'admin@albsigbank.de',
            'password':'Kp96okQBVKn86RCuLJ45HJKjoQ3RRZzp',
            'submit':'Login'}

        r_login = session.post(url + '/login', data=data)
        r_account = session.get(url + '/account')

        admin_soup = BeautifulSoup(r_account.content)
        admin_notes = admin_soup.find('div', {'name':'admin_notes'})

        if admin_notes == None:
            self.error = 1
            self.error_msg = "Login Error."

        else:
            self.error = 0
            data = {'csrf_token':csrf_token,
                    'notes':'ID: ' + str(self.flag_id) + " Flag: " + str(flag),
                    'submit':'Add'}

            r_account = session.post(url + '/account/', data=data)

    def result(self):
        return {'FLAG_ID': self.flag_id,  
                'TOKEN': self.token,
                'ERROR': self.error,
                'ERROR_MSG': self.error_msg}


# debug
if __name__ == "__main__":

    ip = '127.0.0.1'
    port = 5103

    sf_obj = SetFlag()
    sf_obj.execute(ip, port, _flag())
    print(sf_obj.result())

