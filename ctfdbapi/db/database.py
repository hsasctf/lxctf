from sqlalchemy import create_engine, event, inspect
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base

import pymysql
from sqlalchemy.sql.ddl import CreateTable

pymysql.install_as_MySQLdb()

from config import SQLALCHEMY_DATABASE_URI

#engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, pool_pre_ping=True)
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, pool_recycle=280, pool_size=100)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# fill defaults
def instant_defaults_listener(target, args, kwargs):
    for key, column in inspect(target.__class__).columns.items():
        if column.default is not None:
            if callable(column.default.arg):
                setattr(target, key, column.default.arg(target))
            else:
                setattr(target, key, column.default.arg)


event.listen(mapper, 'init', instant_defaults_listener)


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from . import models  # do not delete line
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    from db.models import *
    Base.metadata.create_all(bind=engine)

    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config('/srv/ctf/ctfdbapi/alembic.ini')
    command.stamp(alembic_cfg, "head")
