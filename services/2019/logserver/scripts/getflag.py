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


class GetFlag():

    # GET flag as user flag_id using token collected by set_flag()
    def execute(self, ip, port, flag_id, token):
        assert isinstance(ip, str)
        assert isinstance(port, int) and (0 < port < 2**16)
        assert isinstance(flag_id, str)
        assert isinstance(token, str)

        user_name = flag_id
        self.error_msg = ''
        self.flag = ''
        self.error = 0

        try:
            conn = HTTPConnection(ip, port=port, timeout=10)
            conn.request('GET', '/{}?entries=1'.format(user_name), headers={'Authorization': 'Bearer '+token})

            with closing(conn.getresponse()) as res:
                if res.status == 200:
                    flag = str(res.read())

                    # server appends linefeed at end of msg befroe writing if not present
                    if flag[-1] == '\n': 
                        self.flag = flag[:-1]
                    else:
                        self.flag = flag
                        
                else:
                    raise Exception('bad response: {} {}'.format(res.status, res.read()))

        except Exception as e:
            self.error = 20
            self.error_msg = str(e)

    def result(self):
        return {'FLAG': self.flag,
                'ERROR': self.error,
                'ERROR_MSG': self.error_msg}


if __name__ == '__main__':
    from sys import argv

    gf_obj = GetFlag()
    gf_obj.execute('127.0.0.1', 65333, argv[1], argv[2])
    print(gf_obj.result())