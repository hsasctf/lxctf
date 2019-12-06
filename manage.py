#!/usr/bin/env python3

"""
this script simplifies developing
for a shell in gameserver (web) container run ./manage.py dev shell
for a shell in a team 2 container run ./amange.py dev 2
"""

import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("env", help='dev or game')
parser.add_argument("command", help='shell|[1-254]')
args = parser.parse_args()


if args.env == "game":
    if args.command == "shell":
        subprocess.call("ssh -i sshkey/id_rsa_ctf ctf@10.38.1.1", shell=True)
    else:
        try:
            num = int(args.command)
            subprocess.call("ssh -i sshkey/id_rsa_ctf ubuntu@10.40.{}.1".format(num),
                            shell=True)
        except TypeError:
            print("error")
elif args.env == "dev":
    if args.command == "shell":
        subprocess.call("vagrant ssh -c 'sudo lxc exec web -- sudo --login -u ctf bash'", shell=True)
    else:
        try:
            num = int(args.command)
            subprocess.call("vagrant ssh -c 'sudo lxc exec team{} -- sudo --login -u ubuntu bash'".format(num), shell=True)
        except TypeError:
            print("error")