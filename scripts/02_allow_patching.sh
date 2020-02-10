#!/usr/bin/env bash


# run when game begins

for i in {1..127}
do
   iptables -I FORWARD -s "10.41.$i.0/24" -d "10.40.$i.1" -j ACCEPT -m comment --comment "time for defense"
   iptables -I FORWARD -s "10.42.$i.0/24" -d "10.40.$i.1" -j ACCEPT -m comment --comment "time for defense"
done