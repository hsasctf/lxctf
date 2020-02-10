# Wireguard

Wireguard is a simple and lightweight vpn.


## Varaibles used in this readme

-   &lt;team-id&gt;, the id of the team taking part in the ctf
-   &lt;player-num&gt;, the number of players starting from one and counting to five. Unfourtunatly this is hardcoded.


## Installation and Packages

The associated ansible script installes the following packages on the host:

-   ufw, a simple firewall
-   wireguard-tools, wireguard itself
-   wireguard-dkms, the wireguard kernel module


## Firewall rules

These ufw rules are created when the asible script is executed:

-   ufw allow 42&lt;team-id&gt;/udp
-   ufw allow 42254/udp

Where the rule with &lt;team-id&gt; is added for each team and the ids are prefaced with zeros, so that the whole portnumber is five digits long.


## Directories created

-   *etc/wireguard*

The following directories are created on the host in the context of the ansible directory:

-   files/wireguard/tmp/
-   files/client/configs/
-   files/server/configs/
-   files/client/configs/team&lt;team-id&gt;

Teamfolders are created for each team.


## Key creation

A keypair is generated for teach player in the ctf (five per team), as well as five keys for team 254, the admin team and one keypair fore the server.

These Keypairs are saved in /files/wireguard/tmp/privatekey-&lt;team-id&gt;-player-&lt;player-num&gt; and files/wireguard/tmp/publickey-&lt;team-id&gt;-player-&lt;player-num&gt; for each player. The Server keys are named /files/wireguard/tmp/private-server and /files/wireguard/tmp/publickey-server.


## Building the interface configs

The configuaritonfiles for the wireguard-interfaces are located in *roles/vpn/templates/wireguard* relative to the root of the project.

Before generating the serverconfigs it's necessary to check for the interface, were the server is listening on at /roles/vpn/templates/wireguard/server.conf.j2. The default interface name for applying the forwarding rules on is ens3.

Configs are created for each player are saved to \*files/client/configs/wg1-&lt;team-id&gt;.conf with the prefix wg1- for player 1, wg2- for player two and so on. After that they are transferred to there team-directories in /files/client/configs/&lt;team-id&gt;\*

The serverconfigs are stored in /files/server/configs/wg&lt;team-id&gt;.conf

For the admin configsyou need to change the DNS from 10.40.254.254 to 10.40.&lt;some-team-id&gt;.254 or a public DNS to enable DNS functionality.
Also change allowed ips 10.40.254.254 to your DNS, eg 10.40.1.254. 


## Securing the private keys and starting the server-interfaces

The privatekeys for the clients are made unaccessible via chmod and chown.

    sudo chmod 600 <ansible-path>/files/wireguard_tmp/privatekey-*
    sudo chown root:root <ansible-path>/files/wireguard_tmp/privatekey-*

A last the interfaces on the host are set up for all teams.

    sudo wg-quick up wg&lt;team-id&gt;


## Problems while buliding the ansible infrastructure a second time

The wireguard interfaces are not disabled, so at rebuilding an error occours, that mentions this.
Just execute scripts/04_wireguard_interface_down.sh


## Post using problems

Should you not stop the interface correctly after a session or should something crash your ip-configuration might be broken.
To fix these issues, first disable the interface via

    sudo wg-quick down wg&lt;team-id&gt;

Then delete your ip configuration on the interface, eg. eth0 that shows you an ip like 10.40.1.1/24 with the following command:

    sudo ip addr del 10.40.1.1/24 dev eth0

After that, if you need to start your dhcp client again to get a new ip on you interface.

    sudo dhclient eth0
