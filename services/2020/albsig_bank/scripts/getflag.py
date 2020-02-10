#!/usr/bin/python2.7
#coding: utf-8

from __future__ import print_function
import requests
import re

from bs4 import BeautifulSoup

from random import choice
from string import ascii_lowercase
from contextlib import closing # needed for py2.7 httplib to be used with contextmanager


def _rand_str(length=10):
    return ''.join((choice(ascii_lowercase) for _ in range(length)))


def _flag():
    return 'FLAG_'+_rand_str(13)


class GetFlag():

    # GET flag as user flag_id using token collected by set_flag()
    def execute(self, ip, port, flag_id, token):
        assert isinstance(ip, str)
        assert isinstance(port, int) and (0 < port < 2**16)
        assert isinstance(flag_id, str)
        assert isinstance(token, str)

        url = 'http://' + str(ip) + ':' + str(port)

        session = requests.Session()

        self.error_msg = ''
        self.flag = ''
        self.error = 0

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

        cut_notes=re.search(flag_id + '\sFlag:\sFLAG_[a-z]{13}', str(admin_notes)).group(0)
        flag_note=re.search('FLAG_[a-z]{13}', str(cut_notes)).group(0)

        if flag_note == None:
            self.error = 1
            self.error_msg = "Login Error or Flag was deleted."
        
        else:
            self.error = 0
            self.flag = flag_note

        return

    def result(self):
        return {'FLAG': self.flag,
                'ERROR': self.error,
                'ERROR_MSG': self.error_msg}


if __name__ == '__main__':
    from sys import argv

    gf_obj = GetFlag()
    gf_obj.execute('127.0.0.1', 5103, argv[1], argv[2])
    print(gf_obj.result())
