# Install the infrastructure via Ansible (locally)

## Server OS

Recommended OS is: Xubuntu/Lubuntu 16.04 Desktop 64 Bit



# Root on ZFS

Installed manually as described in https://github.com/zfsonlinux/zfs/wiki/Ubuntu-16.04-Root-on-ZFS

Use `tank` instead of `rpool` in each command!

create dataset `tank/lxd` using `zfs create tank/lxd`

# ZFS Partition

Instead of Root on ZFS it's also possible to have a partition formatted with ZFS with a pool named `tank`.
Then just create the dataset `lxd` using `zfs create tank/lxd`.

## LXD Production setup


https://github.com/lxc/lxd/blob/master/doc/production-setup.md

check syntax and reload `/sbin/sysctl -p`

reboot needed

## Install ctf infrastructure

Clone repo

```bash
sudo apt-get --yes install python3-yaml
sudo ansible-galaxy install -r requirements.yml 
sudo apt install python-pip
sudo pip install ansible
sudo ansible-playbook -i inventories/local site.yml
lxc config set web limits.cpu.priority 9
lxc config set web limits.cpu 4
```

