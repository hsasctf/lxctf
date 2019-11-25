#!/usr/bin/python2.7

# setflag script for ctf logserver

# flag id: random string used as user in requests to logserver
# flag: random string used as single log entry

from __future__ import print_function

from httplib import HTTPConnection
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

        self.flag_id = user_name = _rand_str()
        self.error_msg = ''
        self.token = ''

        try:
            conn = HTTPConnection(ip, port=port, timeout=10)
            conn.request('POST', '/'+user_name, body=flag)
            with closing(conn.getresponse()) as res:
                if res.status == 200:
                    self.token = str(res.read())
                else:
                    raise Exception('bad response: {} {}'.format(res.status, res.read()))
        except Exception as e:
            self.error_msg = str(e)

    def result(self):
        return {'FLAG_ID': self.flag_id,  
                'TOKEN': self.token, 
                'ERROR_MSG': self.error_msg}


# debug
if __name__ == "__main__":

    ip = '127.0.0.1'
    port = 65333

    sf_obj = SetFlag()
    sf_obj.execute(ip, port, _flag())
    print(sf_obj.result())

