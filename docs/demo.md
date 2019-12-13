
## How to run demo

`reinit_project.sh` (if needed)
`vagrant destroy -f` (if needed)
`vagrant up`

repeat `vagrant provision` until there are no Ansible errors

```bash
vagrant ssh gameserver
cd /vagrant/ctfdbapi
python3 demo1.py <minutes until AD starts>
```

Important

- For every question: Enter = Yes
- ctfdbapi needs 2-3 minutes to start completely
