# lxctf

An Ansible project to automate installation and configuration of an Attack/Defense CTF framework (based of iCTF concept and code).

## How to use repo

```
git clone URL
git submodule init
git submodule update
vagrant up
vagrant provision
```

## Components

- Vagrant for development environment
- OpenVPN Server for connections to CTF server
- SQLAlchemy for database connection from Python to MariaDB
- Flask-Admin for database administration
- Ansible scripts for installation
- LXD containers for OS-level virtualization 