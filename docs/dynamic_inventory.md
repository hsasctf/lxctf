# Dynamic inventory

The dynamic Ansible inventory is located in `inventories/ctf.py`. It automatically generates keys and password and saves them in `inventories/ctf_config.yml`.
This ensures that they are unique for every new game. Also a secret string is dynamically derived from the variable `secret` for every team.
Each team VM in the inventory has a dynamic variable `team_secret` which can be used to write secure Ansible scripts with unique keys and passwords for each team.
In `filter_plugins/my_filters.py` one can find a custom Ansible Jinja2 filter that uses this `team_secret` and can be used in Ansible templates/tasks.

For example you want to deploy a web app using mysql then you can set variables in your Ansible play and use them in your templates/tasks:

```yaml

- set_fact:
    mysql_root_password: "{{ team_secret | ctf_hmac('safe_file_check', 'mysql_root_password') }}"
    mysql_safe_file_check_password: "{{ team_secret | ctf_hmac('safe_file_check', 'mysql_safe_file_check_password') }}"

```

First argument should be the name of the service, the second is how the key/password is used.

Except for `team_count`, the file `ctf_config.yml` must not be changed.