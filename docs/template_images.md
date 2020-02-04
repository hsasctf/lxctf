# Template Images

## Types

- AD image container: 10.30.1.1 (tpl1)
- Jeopary image container: 10.30.2.1 (tpl2) (UNFINISHED)


## Create team containers from prepared image

1. login to AD image container and install all services
1. make sure the service listens to 0.0.0.0
1. on host **delete** the team containers e.g. `lxc list -c n --format csv | grep team | xargs -i"{}" lxc delete {} --force`
1. run ansible-playbook (`vagrant provision` for dev, for local installation see `local.md`)