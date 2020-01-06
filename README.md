[![Build Status](https://travis-ci.com/hsasctf/lxctf.svg?branch=master)](https://travis-ci.com/hsasctf/lxctf)

# lxctf

Attack/Defense CTF framework that is based on iCTF concept and code.

Unlike iCTF, we are not creating VirtualBox images or setup cloud servers for the teams. Instead, we setup machine containers (LXD) with networking on a single machine where the CTF takes place.  
 

## How to install the development environment

```
git clone URL
git submodule init
git submodule update
./reinit_project.sh
vagrant up
vagrant provision
```

## Upgrade

```
git pull master
git submodule update
```

## Components

- Vagrant for development environment
- OpenVPN + Wireguard Server for connections to CTF server
- SQLAlchemy for database connection from Python to MariaDB
- Flask-Admin for database administration
- Ansible scripts for installation
- LXD containers for OS-level virtualization 