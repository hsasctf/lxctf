# Change Database scheme

## Edit models.py

## Autogenerate Migration file

```
cd /vagrant/ctfdbapi
PYTHONPATH=. alembic revision --autogenerate
```



## Change DB revision to head


```
cd /vagrant/ctfdbapi
PYTHONPATH=. alembic upgrade head
```




# How to run own scripts

```
cd /vagrant/ctfdbapi
PYTHONPATH=. python3 db/<script>.py
``` 

# Backup database to Ansible role  (in development environment)

```
mysqldump -uroot -p ctf > /vagrant/roles/mariadb/ctf_dump.sql
```
