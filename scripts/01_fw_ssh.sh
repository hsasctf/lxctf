#!/usr/bin/env bash


# run before handing out SSH keys / openvpn keys

for i in {1..127}
do
   iptables -I FORWARD -s 10.40.0.0/16,10.41.0.0/17,10.42.0.0/17 -d "10.40.$i.1" -j DROP -m comment --comment "block ssh"
done