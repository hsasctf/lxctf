#!/usr/bin/python2.7

# getflag script for ctf pwstore REST-Api

# flag id: random string used as user in requests pwstore api
# flag: random string used as single pw entry

from __future__ import print_function

from httplib import HTTPConnection
import json

class GetFlag():

    def execute(self, ip, port, flag_id, token):
        assert isinstance(ip, str)
        assert isinstance(port, int) and (0 < port < 2**16)
        assert isinstance(flag_id, str)
        assert isinstance(token, tuple) and len(token)==2

        self.flag = ''
        self.error_msg = ''
        self.error = -1

        masterpw, pw_id = token

        getentry_json = json.dumps({
            'username': flag_id,
            'masterpw': masterpw,
            'pw_id': pw_id
        })

        try:
            conn = HTTPConnection(ip, port=port, timeout=10)
            headers = {'Content-type': 'application/json'}

            conn.request('GET', '/getentry', headers=headers, body=getentry_json)
            res = conn.getresponse()
            if res.status == 200:
                data = json.loads(res.read())
                self.flag = data['pw_entry']['pw']
                self.error = 0
            else:
                self.error = 1
                raise Exception('/getentry failed: ' + str(res.status) + ': ' + res.read())

        except Exception as e:
            self.error = -1
            self.error_msg = str(type(e)) + ': ' + str(e)

        finally:
            try:
                conn.close()
            except:
                pass

    def result(self):
        return {'FLAG': self.flag or '',
                'ERROR': self.error or -1,
                'ERROR_MSG': self.error_msg or ''}


# debug
if __name__ == "__main__":

    from sys import argv

    ip = '10.40.1.1'
    port = 5102

    if len(argv) == 4:
        flag_id = argv[1]
        token = (argv[2], argv[3])
    else:
        flag_id = 'some_flag_id'
        token = ('some_masterpw', 'some_pw_id')

    sf_obj = GetFlag()
    sf_obj.execute(ip, port, flag_id, token)
    print(sf_obj.result())

