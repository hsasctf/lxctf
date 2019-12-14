
# Table of Contents

1.  [Wireguard](#org843b4b0)
    1.  [Varaibles used in this readme](#org6c7ba28)
    2.  [Installation and Packages](#org21fd0fc)
    3.  [Firewall rules](#org90e0eee)
    4.  [Directories created](#org31859cc)
    5.  [Key creation](#org1f1a100)
    6.  [Building the interface configs](#org8b799f2)
    7.  [Securing the private keys and starting the Server-interfaces](#org1dd0229)


<a id="org843b4b0"></a>

# Wireguard

Wireguard is a simple and lightweight vpn.


<a id="org6c7ba28"></a>

## Varaibles used in this readme

-   &lt;team-id&gt;, the id of the team taking part in the ctf
-   &lt;player-num&gt;, the number of players starting from one and counting to five. Unfourtunatly this is hardcoded.


<a id="org21fd0fc"></a>

## Installation and Packages

The associated ansible script installes the following packages on the host:

-   ufw, a simple firewall
-   wireguard-tools, wireguard itself
-   wireguard-dkms, the wireguard kernel module


<a id="org90e0eee"></a>

## Firewall rules

These ufw rules are created when the asible script is executed:

-   ufw allow 42&lt;team-id&gt;/udp
-   ufw allow 42254/udp

Where the rule with &lt;team-id&gt; is added for each team and the ids are prefaced with zeros, so that the whole portnumber is five digits long.


<a id="org31859cc"></a>

## Directories created

-   *etc/wireguard*

The following directories are created on the host in the context of the ansible directory:

-   files/wireguard/tmp/
-   files/client/configs/
-   files/server/configs/
-   files/client/configs/team&lt;team-id&gt;

Teamfolders are created for each team.


<a id="org1f1a100"></a>

## Key creation

A keypair is generated for teach player in the ctf (five per team), as well as five keys for team 254, the admin team and one keypair fore the server.

These Keypairs are saved in /files/wireguard/tmp/privatekey-&lt;team-id&gt;-player-&lt;player-num&gt; and files/wireguard/tmp/publickey-&lt;team-id&gt;-player-&lt;player-num&gt; for each player. The Server keys are named /files/wireguard/tmp/private-server and /files/wireguard/tmp/publickey-server.


<a id="org8b799f2"></a>

## Building the interface configs

The configuaritonfiles for the wireguard-interfaces are located in *roles/vpn/templates/wireguard* relative to the root of the project.

Before generating the serverconfigs it's necessary to check for the interface, were the server is listening on at /roles/vpn/templates/wireguard/server.conf.j2. The default interface name for applying the forwarding rules on is ens3.

Configs are created for each player are saved to \*files/client/configs/wg1-&lt;team-id&gt;.conf with the prefix wg1- for player 1, wg2- for player two and so on. After that they are transferred to there team-directories in /files/client/configs/&lt;team-id&gt;\*

The serverconfigs are stored in /files/server/configs/wg&lt;team-id&gt;.conf


<a id="org1dd0229"></a>

## Securing the private keys and starting the Server-interfaces

The privatekeys for the clients are made unaccessible via chmod and chown.

    sudo chmod 600 <ansible-path>/files/wireguard_tmp/privatekey-*
    sudo chown root:root <ansible-path>/files/wireguard_tmp/privatekey-*

A last the interfaces on the host are set up for all teams.

    sudo wg-quick up wg<team-id>

