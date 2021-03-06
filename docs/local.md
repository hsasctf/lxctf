# Install the infrastructure via Ansible (locally)

## Server OS

Recommended (tested) OS is: Xubuntu/Lubuntu 16.04 Desktop 64 Bit

# Root on ZFS

Installed manually as described in https://github.com/zfsonlinux/zfs/wiki/Ubuntu-16.04-Root-on-ZFS

create dataset `rpool/lxd` using `zfs create rpool/lxd`

# ZFS Partition

Instead of Root on ZFS it's also possible to have a partition formatted with ZFS with a pool named `rpool`.
Then just create the dataset `lxd` using `zfs create rpool/lxd`.

## LXD Production setup

This step is important since the gameserver does tens of thousands of file operations.

https://github.com/lxc/lxd/blob/master/doc/production-setup.md

check syntax and reload `/sbin/sysctl -p`

reboot needed

## Install ctf infrastructure

1. Clone repo

```bash
sudo apt-get --yes install python3-yaml python-yaml python-pip
sudo ansible-galaxy install -r requirements.yml 
sudo pip install ansible==2.8.6
sudo ansible-playbook -i inventories/ctf.py --key-file <path to lxctf>/sshkey/id_rsa_ctf site.yml
lxc config set web limits.cpu.priority 9
lxc config set web limits.cpu 4
```

set `team_count` in `inventories/ctf_config.yml` to correct number of teams and **rerun the `ansible-playbook` command untils there are no errrors**