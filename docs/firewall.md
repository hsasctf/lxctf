
# Table of Contents

1.  [Firewall](#org4561048)
    1.  [Varaibles used in this readme](#org69d77fe)
    2.  [Initial configurations](#orge234c04)
    3.  [Input chain](#org1a0f89c)
    4.  [Forward chain](#org82fb6e7)
    5.  [Last steps](#org2688379)


<a id="org4561048"></a>

# Firewall

Iptables is used as firewall to secure the host system and control request forwarded to the lxc containers.
Please notice that ansible **configures your local firewall** if you install this in productive environment.


<a id="org69d77fe"></a>

## Varaibles used in this readme

-   **<team-id>**, the id of the team taking part in the ctf
-   **<service-port>**, all ports ment for attackable services (can be specified in roles/firewall/vars/main.yml)


<a id="orge234c04"></a>

## Initial configurations

In the beginning iptables is installed, if not present already.
Ipv6 is disabled via sysctl to only allow ipv4 packages also ip-forwarding is enabled for ipv4.
All rules in the INPUT, FORWARD and OUTPUT chain are **flushed**.

The default policies for INPUT-/ FORWARD-chain are set to REJECT/ DROP, thus making them **whitelists**.


<a id="org1a0f89c"></a>

## Input chain

The following packages are accepted:

-   TCP ESTABLISHED, RELATED on any port
-   TCP SYN on port 22


<a id="org82fb6e7"></a>

## Forward chain

The following packages are accepted:

-   TCP ESTABLISHED, RELATED
-   TCP SYN from **10.42.<team-id>.1-10.42.<team-id>.5** to **10.40.<team-id>.0/24** port 22
-   TCP SYN from **10.42.<team-id>.1-10.42.<team-id>.5** to **10.40.<team-id>.0/24** port <service-port>
-   UDP from **10.42.<team-id>.1-10.42.<team-id>.5** to **10.40.<team-id>.0/24** port <service-port>
-   UDP from **10.40.<team-id>.0/24** to **10.42.<team-id>.1-10.42.<team-id>.5** port <service-port>
-   TCP SYN from **10.42.<team-id>.1-10.42.<team-id>.5** to **10.39.<team-id>.0/24** port 22
-   TCP from **10.42.<team-id>.1-10.42.<team-id>.5** to **10.38.<team-id>.0/24**
-   UDP from **10.42.<team-id>.1-10.42.<team-id>.5** to **10.38.<team-id>.0/24**


<a id="org2688379"></a>

## Last steps

Iptables is enabled via systemctl and the configuration is exported to  <ansible-path>/files/iptables.fw.

