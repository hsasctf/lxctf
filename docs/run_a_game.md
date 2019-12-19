Several days before the game
============================

Registration
------------

-   Add Event to database using flask-admin
    -   vpn team254, <http://10.38.1.1:4999/admin/>
    -   maybe port 5000 from another team\'s VPN
-   start registration app
-   disseminate URL to registration
    -   same host register app: url is <http://default_ip:80> (there is
        a DNAT rule to 10.38.1.1:4998)
    -   when there is no automated registration: add Teams to db, then
        AttendingTeams with the correct event

Service Deployment
------------------

See `service_requirements.md`

### Write the service code

### Write getflag/setflag scripts and test with dev environment

### Write Ansible code for deployment and test with dev environment

### Add services to database

Add Challenges: `python3 manage_add_services.py` to upload scorebot
scripts and service info to DB. This reads flagscripts of services from
the services/directory, and metadata from json and adds the info/scripts
to the DB.

Test run / Day of the game
==========================

*!! scripts/\*.sh must be run on host system, not in containers*

*!! tmux commands must be run inside web container*

-   run `scripts/00_snapshot.sh` for a snapshot before testing

-   run the commands in web container:

``` {.bash}
# Dashboard + Web APIs to access the database from Scorebot
tmux new -d -s ctfdbapi -- 'keep-one-running python3 /opt/ctfdbapi/tornado_file.py'  \; pipe-pane 'cat >> /var/log/ctf/tornado.log'

# Each round is started by Gamebot
tmux new -d -s gamebot -- 'keep-one-running python3 /opt/ctfdbapi/gamebot.py'

# Caches scores fetched from database to redis. Redis db is used in the dashboard (via Web API)
tmux new -d -s dashboard_worker -- 'keep-one-running python3 /opt/ctfdbapi/dashboard_worker.py'
```

-   run `scripts/01_fw_ssh.sh` to prevent access to SSH (for teams)
-   last step should be before Event.start (in database)
-   after Event.start the register app allows for download of keys (implemented but UNTESTED)
-   run `scripts/02_allow_patching.sh` to allow teams to connect via SSH
    for service patching
-   run `scripts/03_allow_attack.sh` after `Event.attack_defense_start` in
    database. allows team-to-team connections (attacks).
-   Start scorebot using `tmux new -d -s scorebot -- 'keep-one-running python2 /opt/scorebot/scorebot.py'` after Gamebot has created the first tick
-   if this was a test run you can run `scripts/99_restore.sh` for
    another test run or for the real game (snapshot rollback)
