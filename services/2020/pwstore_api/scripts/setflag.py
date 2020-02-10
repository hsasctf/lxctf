#!/usr/bin/python2.7

# setflag script for ctf pwstore REST-Api

# flag id: random string used as user in requests pwstore api
# flag: random string used as single pw entry

from __future__ import print_function

from httplib import HTTPConnection
from random import choice
from string import ascii_letters
import json


def _rand_str(length=10):
    return ''.join((choice(ascii_letters) for _ in range(length)))


def _flag():
    return 'FLAG_'+_rand_str(13)


class SetFlag():

    def execute(self, ip, port, flag):
        assert isinstance(ip, str)
        assert isinstance(port, int) and (0 < port < 2**16)

        self.flag_id = user_name = _rand_str()
        self.error_msg = ''
        self.error = -1
        self.token = (None, None)

        masterpw = _rand_str()

        register_json = json.dumps({
            'username': user_name,
            'masterpw': masterpw,
        })

        addentry_json = json.dumps({
            'username': user_name,
            'masterpw': masterpw,
            'pw_entry': flag,
            'description' : 'scorebot_flag',
        })

        try:
            conn = HTTPConnection(ip, port=port, timeout=10)
            headers = {'Content-type': 'application/json'}

            conn.request('POST', '/register', headers=headers, body=register_json)
            res = conn.getresponse()
            if res.status == 201:
                # have to completely read res body before next request even if unused (httplib requirement)
                _ = res.read()
            else:
                raise Exception('/register failed: ' + str(res.status) + ': ' + res.read())

            conn.request('PUT', '/addentry', headers=headers, body=addentry_json)
            res = conn.getresponse()
            if res.status == 201:
                # remember masterpw, pw_id for getflag
                data = json.load(res)
                self.token = (masterpw, str(data['pw_entry']['pw_id']))
                self.error = 0
            else:
                self.error = 1
                raise Exception('/addentry failed: ' + str(res.status) + ': ' + res.read())

        except Exception as e:
            self.error_msg = str(type(e)) + ': ' + str(e)

        finally:
            try:
                conn.close()
            except:
                pass

    def result(self):
        return {
            'FLAG_ID': self.flag_id,  
            'TOKEN': self.token, 
            'ERROR': self.error,
            'ERROR_MSG': self.error_msg or '',
        }


# debug
if __name__ == "__main__":

    ip = '10.40.1.1'
    port = 5102

    sf_obj = SetFlag()
    sf_obj.execute(ip, port, _flag())
    print(sf_obj.result())

