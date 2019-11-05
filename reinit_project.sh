#!/usr/bin/env bash

rm -rf roles/vpn/files/*_configs roles/vpn/files/vpn_tempfiles
rm -rf roles/infrastructure_lxd/files/*_keys
rm -rf roles/infrastructure_lxd/files/lxd.{key,cert}
mkdir -p roles/infrastructure_lxd/files/
mkdir -p sshkey
ssh-keygen -t rsa -b 2048 -C "ctf developer" -f sshkey/id_rsa_ctf -P '' -q
