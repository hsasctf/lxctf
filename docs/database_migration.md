# Change Database scheme

## Edit models.py

## Autogenerate Migration file

```
cd /srv/ctf/ctfdbapi
PYTHONPATH=. alembic revision --autogenerate
```



## Change DB revision to head


```
cd /srv/ctf/ctfdbapi
PYTHONPATH=. alembic upgrade head
```




# How to run own scripts

```
cd /srv/ctf/ctfdbapi
PYTHONPATH=. python3 db/<script>.py
``` 

# Backup database to Ansible role  (in development environment)

```
mysqldump -uroot -p ctf > /srv/ctf/roles/mariadb/ctf_dump.sql
```
