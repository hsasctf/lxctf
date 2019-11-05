#!/usr/bin/python

from __future__ import unicode_literals
import hashlib
import base64


class FilterModule(object):
    def filters(self):
        return {
            'ctf_hmac': self.ctf_hmac
        }

    def ctf_hmac(self, team_secret, service, use):
        if any(len(x) == 0 for x in [team_secret, service, use]):
            raise ValueError("Fill all 3 Parameters with strings")
        return base64.b64encode(hashlib.pbkdf2_hmac('sha256', team_secret.encode("utf8"), service.encode("utf8")+"||".encode("utf8")+use.encode("utf8"), 100))

        
