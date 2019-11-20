#!/usr/bin/env python3

'''
CTF dynamic inventory script for Ansible
'''

import base64
import hashlib
import os
import random
import string
import sys
import argparse
import yaml

import os

with open("/tmp/env", "w") as fp:
    for param in os.environ.keys():
        fp.write("%20s %s\n" % (param, os.environ[param]))

try:
    import json
except ImportError:
    import simplejson as json


def is_dev():
    """
    check if the machine running Ansible is the controller VM of the development environment
    :return: True if Ansible runs in controller VM, else False
    """
    from subprocess import check_output
    try:
        ips = check_output(['hostname', '--all-ip-addresses'])
        ips = ips.split()
        if b"172.16.17.5" in ips:
            return True
    except Exception as e:
        print(repr(e))
    return False


IS_DEV = is_dev()

possible_characters = string.ascii_letters + string.digits


def generate_password(length=32):
    rng = random.SystemRandom()
    return "".join([rng.choice(possible_characters) for i in range(length)])


def default_config():
    return {
        "secret": generate_password(),  # some passwords will derive from this
        "dashboard_admin_password": generate_password(),
        "api_secret": generate_password(),
        "lxd_trust_pw": generate_password(),
        "mysql_root_password": generate_password(),
        "mysql_ctf_password": generate_password(),
        "team_count": 2,
    }


def generate_team_secret(secret, num):
    num = str(num)
    return base64.b64encode(hashlib.pbkdf2_hmac('sha256', secret.encode("utf8"),
                                                num.encode("utf8"),
                                                100)).decode()


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ctf_config.yml")
if not os.path.exists(config_path):
    with open(config_path, "w") as fp:
        yaml.dump(default_config(), fp, default_flow_style=False)

with open(config_path, 'r') as stream:
    GLOBAL_CONFIG = yaml.safe_load(stream)

ctfdev_config_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vagrant_ctfdev_config.local.yml")
ctfdev_config_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vagrant_ctfdev_config.yml")

try:
    with open(ctfdev_config_path1, "r") as stream:
        CTFDEV_CONFIG = yaml.safe_load(stream)
except:
    with open(ctfdev_config_path2, "r") as stream:
        CTFDEV_CONFIG = yaml.safe_load(stream)


class CtfInventory(object):

    def __init__(self):

        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.ctf_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))

    # Example inventory for testing.
    def ctf_inventory(self):
        return {
            "_meta": {
                "hostvars": {
                    "172.16.17.10" if IS_DEV else "127.0.0.1": {
                        "ansible_connection": "ssh",
                        "ansible_ssh_port": 22,
                        "ansible_ssh_private_key_file": "/vagrant/.vagrant/machines/ctfserver/libvirt/private_key",
                        "ansible_ssh_user": "vagrant",
                        "lxd_proxy_host": "127.0.0.1:8445",
                        "lxd_trust_pw": GLOBAL_CONFIG['lxd_trust_pw'],
                        "lxd_zfs_pool": "tank/lxd",
                        "secret": GLOBAL_CONFIG['secret']
                    },
                    "controller": {
                        "ansible_connection": "local"
                    },
                    "jeop1": {
                        "ansible_connection": "ssh",
                        "ansible_host": "10.39.1.1",
                        "ansible_ssh_common_args": "-o StrictHostKeyChecking=no" if not IS_DEV else "-o ProxyCommand=\"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /vagrant/.vagrant/machines/ctfserver/libvirt/private_key -W %h:%p -q vagrant@172.16.17.10\"",
                        "ansible_ssh_private_key_file": "" if not IS_DEV else "/vagrant/sshkey/id_rsa_ctf",
                        "ansible_ssh_user": "ubuntu",
                        "jeop_num": 1
                    },
                    # include n teams in dict
                    **{
                        "team{}".format(i): {
                            "ansible_connection": "ssh",
                            "ansible_host": "10.40.{}.1".format(i),
                            "ansible_ssh_common_args": "-o StrictHostKeyChecking=no" if not IS_DEV else "-o ProxyCommand=\"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /vagrant/.vagrant/machines/ctfserver/libvirt/private_key -W %h:%p -q vagrant@172.16.17.10\"",
                            "ansible_ssh_private_key_file": "" if not IS_DEV else "/vagrant/sshkey/id_rsa_ctf",
                            "ansible_ssh_user": "ubuntu",
                            "team_num": i,
                            "team_secret": generate_team_secret(GLOBAL_CONFIG['secret'], i)
                        } for i in range(1, GLOBAL_CONFIG['team_count'] + 1)
                    },
                    "web": {
                        "ansible_connection": "ssh",
                        "ansible_host": "10.38.1.1",
                        "ansible_ssh_common_args": "-o StrictHostKeyChecking=no" if not IS_DEV else "-o ProxyCommand=\"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i /vagrant/.vagrant/machines/ctfserver/libvirt/private_key -W %h:%p -q vagrant@172.16.17.10\"",
                        "ansible_ssh_private_key_file": "" if not IS_DEV else "/vagrant/sshkey/id_rsa_ctf",
                        "ansible_ssh_user": "ubuntu",
                        "mysql_ctf_password": GLOBAL_CONFIG['mysql_ctf_password'],
                        "mysql_root_password": GLOBAL_CONFIG['mysql_root_password']
                    }
                }
            },
            "ad_containers": {
                "hosts": [
                    "team1",
                    "team2"
                ]
            },
            "all": {
                "children": [
                    "ad_containers",
                    "ctfserver",
                    "game_containers",
                    "jeop_containers",
                    "ungrouped"
                ]
            },
            "ctfserver": {
                "hosts": [
                    "172.16.17.10" if IS_DEV else "127.0.0.1"
                ]
            },
            "game_containers": {
                "hosts": [
                    "web"
                ]
            },
            "jeop_containers": {
                "hosts": [
                    "jeop1"
                ]
            },
            "ungrouped": {
                "hosts": [
                    "controller"
                ]
            }
        }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


# Get the inventory.
CtfInventory()
