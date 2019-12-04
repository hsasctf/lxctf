# Development

## Development Environment


Consists of 1 VM hosting multiple LXD containers
- 172.16.17.10 ctfserver running LXD and OpenVPN servers
    - LXD container `web` on 10.38.1.1: runs the gameserver (Scorebot, Gamebot, Dashboard)
    - LXD containers `team1` -- `team253`, with IP addresses 10.40.1-253.1: containers für teams



### Vagrant Commands

Delete all VMs: `vagrant destroy -f`

Suspend then Resume: `vagrant suspend` -> `vagrant resume`

Halt then Up: `vagrant halt` -> `vagrant up`

SSH to VM: `vagrant ssh`


### Setup development environment

1. run `reinit_project.sh` to delete old files and generate SSH key
1. run `apt -y install ruby-dev `


#### Using VirtualBox

1. This project was only tested with VirtualBox **5.x** and **6.x**
1. `sudo vagrant plugin install vagrant-disksize`


#### Using libvirt

1. `sudo vagrant plugin install vagrant-libvirt`
1. Create a local config file:

```bash
cat > vagrant_ctfdev_config.local.yml << EOF
provider: libvirt
ctfserver_disk: 120
ctfserver_ram: 2048
ctfserver_cpu: 2
EOF
```

1. Set the environment variable for Vagrant `export VAGRANT_DEFAULT_PROVIDER="libvirt"`


#### Using both

##### Switch from VirtualBox to libvirt

1. `vagrant destroy -f`
1. Delete the Host Network in Global Tools in VirtualBox

![Delete this network to use libvirt instead of VirtualBox](https://i.imgur.com/SmBmtCD.png)

##### Switch from libvirt to VirtualBox

1. Install Virtual Machine Manager
1. Edit -> Connection Details -> Network Interfaces
1. Delete the `ctfa0` network

![Delete the `ctfa0` network to use VirtualBox instead of libvirt](https://i.imgur.com/y0n7wHb.png)

#### Remaining steps

1. libvirt: run `vagrant up`, if provisioning fails it's possible to retry with `vagrant provision` (try again in 5-30 minutes)
1. after changing ansible roles run `vagrant provision`
1. run `vagrant ssh ctfserver` for SSH Shell
    1. in development this VM only contains Team-Containers
    1. in SSH run `lxc list` for a list of containers
    1. Ignore this message from LXD: "If this is your first time using LXD, you should also run: lxd init"
    1. `lxc exec NAME bash` for opening (root) bash in containers
1. run `lxc exec web bash` for starting a shell in the gameserver container *web*. Gameserver code is mounted from Vagrant folder to container `web` in path `/srv/ctf`.
    tmux is the recommended tool to run all gameserver services for development
    
    - to exit tmux use CTRL+b then d
    - open existing tmux session: `tmux -s sessionname`
    - exit session: `tmux kill-session -t sessionname`



    ```bash

    # Dashboard + Web APIs to access the database from Scorebot
    tmux new -d -s ctfdbapi -- 'keep-one-running python3 /opt/ctfdbapi/tornado_file.py'  \; pipe-pane 'cat >> /var/log/ctf/tornado.log'
    
    # Each round is started by Gamebot
    tmux new -d -s gamebot -- 'keep-one-running python3 /opt/ctfdbapi/gamebot.py'

    # Caches scores fetched from database to redis. Redis db is used in the dashboard (via Web API)
    tmux new -d -s dashboard_worker -- 'keep-one-running python3 /opt/ctfdbapi/dashboard_worker.py'

    # Each round Scorebot sends flags to database and services. Getting flags is also tested.
    tmux new -d -s scorebot -- 'keep-one-running python /opt/scorebot/scorebot.py'

    ```



1. connect (from host) to openvpn using `openvpn --config roles/vpn/files/client_configs/client-teamXXX.ovpn`
1. http://10.38.1.1:5000/ (Webapp for CTF teams with flag input, scores).
1. The containers have the timezone UTC, so Attack&Defense Start timestamp must be specified in UTC in the database
1. Admin interface http://10.38.1.1:4999/admin (username: `admin` password: value from `dashboard_admin_password` in `inventories/ctf_config.yml`)



## Gameserver VM

/opt/scorebot/ -> run scorebot with python (python 2)

/opt/ctfdbapi/tornoado_file.py -> DB API/Scoreboard (run with python3)

/opt/ctfdbapi/dashboard_worker.py -> Dashboard worker (run with python3)

/opt/ctfdbapi/gamebot.py -> run with python3

