
# Table of Contents

1.  [Wireguard](#org7da9407)
    1.  [Varaibles used in this readme](#org96011ce)
    2.  [Installation and Packages](#org43121e3)
    3.  [Firewall rules](#orgeb2c7e7)
    4.  [Directories created](#org9da1950)
    5.  [Key creation](#orgbcdebce)
    6.  [Building the interface configs](#orgf314024)
    7.  [Securing the private keys and starting the Server-interfaces](#org3537131)


<a id="org7da9407"></a>

# Wireguard

Wireguard is a simple and lightweight vpn.


<a id="org96011ce"></a>

## Varaibles used in this readme

-   <team-id>, the id of the team taking part in the ctf
-   <player-num>, the number of players starting from one and counting to five. Unfourtunatly this is hardcoded.


<a id="org43121e3"></a>

## Installation and Packages

The associated ansible script installes the following packages on the host:

-   ufw, a simple firewall
-   wireguard-tools, wireguard itself
-   wireguard-dkms, the wireguard kernel module


<a id="orgeb2c7e7"></a>

## Firewall rules

These ufw rules are created when the asible script is executed:

-   ufw allow 42<team-id>/udp
-   ufw allow 42254/udp

Where the rule with <team-id> is added for each team and the ids are prefaced with zeros, so that the whole portnumber is five digits long.


<a id="org9da1950"></a>

## Directories created

-   *etc/wireguard*

The following directories are created on the host in the context of the ansible directory:

-   files/wireguard<sub>tmp</sub>/
-   files/client<sub>configs</sub>/
-   files/server<sub>configs</sub>/
-   files/client<sub>configs</sub>/team<team-id>

Teamfolders are created for each team.


<a id="orgbcdebce"></a>

## Key creation

A keypair is generated for teach player in the ctf (five per team), as well as five keys for team 254, the admin team and one keypair fore the server.

These Keypairs are saved in /files/wireguard<sub>tmp</sub>/privatekey-<team-id>-player-<player-num> and files/wireguard<sub>tmp</sub>/publickey-<team-id>-player-<player-num> for each player. The Server keys are named /files/wireguard<sub>tmp</sub>/private-server and /files/wireguard<sub>tmp</sub>/publickey-server.


<a id="orgf314024"></a>

## Building the interface configs

The configuaritonfiles for the wireguard-interfaces are located in *roles/vpn/templates/wireguard* relative to the root of the project.

Configs are created for each player are saved to *files/client<sub>configs</sub>/wg1-<team-id>.conf with the prefix wg1- for player 1, wg2- for player two and so on. After that they are transferred to there team-directories in /files/client<sub>configs</sub>/<team-id>*

The serverconfigs are stored in /files/server<sub>configs</sub>/wg<team-id>.conf


<a id="org3537131"></a>

## Securing the private keys and starting the Server-interfaces

The privatekeys for the clients are made unaccessible via chmod and chown.

    sudo chmod 600 <ansible-path>/files/wireguard_tmp/privatekey-*
    sudo chown root:root <ansible-path>/files/wireguard_tmp/privatekey-*

A last the interfaces on the host are set up for all teams.

    sudo wg-quick up wg<team-id>

