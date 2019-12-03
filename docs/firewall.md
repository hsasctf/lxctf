
# Table of Contents

1.  [Firewall](#org9e0cd98)
    1.  [Varaibles used in this readme](#org5b46007)
    2.  [Initial configurations](#orgec51c43)
    3.  [Input chain](#org7d1c2e8)
    4.  [Forward chain](#org82c5d05)
    5.  [Last steps](#org9c39c9a)


<a id="org9e0cd98"></a>

# Firewall

Iptables is used as firewall to secure the host system and control request forwarded to the lxc containers.
Please notice that ansible **configures your local firewall** if you install this in productive environment.


<a id="org5b46007"></a>

## Varaibles used in this readme

-   <team-id>, the id of the team taking part in the ctf
-   <service-port>, all ports ment for attackable services (can be specified in roles/firewall/vars/main.yml)


<a id="orgec51c43"></a>

## Initial configurations

In the beginning iptables is installed, if not present already.
Ipv6 is disabled via sysctl to only allow ipv4 packages also ip forwarding is enabled for ipv4.
All rules in the INPUT, FORWARD and OUTPUT chain are **flushed**.

The default policies for INPUT-/ FORWARD-chain are set to REJECT/ DROP, thus making them **whitelists**.


<a id="org7d1c2e8"></a>

## Input chain

The following packages are accepted:

-   TCP ESTABLISHED, RELATED on any port
-   TCP SYN packets on port 22


<a id="org82c5d05"></a>

## Forward chain

The following packages are accepted:

-   TCP ESTABLISHED, RELATED
-   TCP SYN packets from 10.42.<team-id>.1-10.42.<team-id>.5 to 10.40.<team-id>.0/24 port 22
-   TCP SYN packets from 10.42.<team-id>.1-10.42.<team-id>.5 to 10.40.<team-id>.0/24 port <service-port>
-   UDP packets from 10.42.<team-id>.1-10.42.<team-id>.5 to 10.40.<team-id>.0/24 port <service-port>
-   UDP packets from 10.40.<team-id>.0/24 to 10.42.<team-id>.1-10.42.<team-id>.5 port <service-port>
-   TCP SYN packets from 10.42.<team-id>.1-10.42.<team-id>.5 to 10.39.<team-id>.0/24 port 22
-   TCP packets from 10.42.<team-id>.1-10.42.<team-id>.5 to 10.38.<team-id>.0/24
-   UDP packets from 10.42.<team-id>.1-10.42.<team-id>.5 to 10.38.<team-id>.0/24


<a id="org9c39c9a"></a>

## Last steps

Iptables is enabled via systemctl and the configuration is exported to  <ansible-path>/files/iptables.fw.

