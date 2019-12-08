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



# Migrate the `cleaning/cleanDB` branch

Once logged in on the **web** lxc container, following steps are necessary:

Due to DB key issues, modifying the `models.py` needs to be seperated in several steps.

1. > ### Export Python Path
   > execute
   > ```sh 
   > root@web:/$ export PYTHONPATH=/srv/ctf/ctfdbapi
   > ```

2. > ### Remove the class `FoodSize` in `models.py`.
   > delete following lines in `models.py`:
   > ```python
   > class FoodSize(enum.Enum):
   >    small = 1
   >    large = 2
   > ...
   >    size = Column(Enum(FoodSize), default=2, nullable=False)
   > ```
   > create alembic script in `/srv/ctf/ctfdbapi`
   > ```sh 
   > root@web:ctfdbapi$ alembic revision --outogenerate -m 'remove_foodsize'
   > ```
   > change revision in `/src/ctf/ctfdbapi`
   > ```sh
   > root@web:ctfdbapi$ alembic upgrade head
   > ```
   
3. > ### Remove the class `Food` in `models.py`.
   > delete following lines in `models.py`:
   > ```python
   > class Food(ModelBase):
   >     __tablename__ = "food"
   >
   >     name = Column(String(64))
   >     price = Column(DECIMAL(4, 2))
   >
   >     def __str__(self):
   >         return "Food {}".format(self.name)
   > ...
   >     food_id = Column(Integer, ForeignKey('food.id', ondelete='CASCADE'), nullable=False)
   >     food = relationship('Food',
   >         backref=backref('caterings', cascade="all, delete-orphan", lazy='dynamic'))
   > ...
   >     def __str__(self):
   >         return "Food {}".format(self.food)
   > ```
   > create alembic script in `/srv/ctf/ctfdbapi`
   > ```sh 
   > root@web:ctfdbapi$ alembic revision --outogenerate -m 'remove_food'
   > ```
   > change revision in `/src/ctf/ctfdbapi`
   > ```sh
   > root@web:ctfdbapi$ alembic upgrade head
   > ```
   
4. > ### Remove the class `Catering` in `models.py`.
   > delete following lines in `models.py`:
   > ```python
   > class Catering(ModelBase):
   >     __tablename__ = "catering"
   >
   >     event_id = Column(Integer, ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
   >     event = relationship('Event',
   >         backref=backref('caterings', cascade="all, delete-orphan", lazy='dynamic'))
   >
   >     user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
   >     user = relationship('User',
   >         backref=backref('caterings', cascade="all, delete-orphan", lazy='dynamic'))
   > ```
   > create alembic script in `/srv/ctf/ctfdbapi`
   > ```sh 
   > root@web:ctfdbapi$ alembic revision --outogenerate -m 'remove_catering'
   > ```
   > change revision in `/src/ctf/ctfdbapi`
   > ```sh
   > root@web:ctfdbapi$ alembic upgrade head
   > ```
