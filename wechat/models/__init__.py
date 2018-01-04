#! -*- coding: utf-8 -*-
import logging
import sqlalchemy
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker
from wechat import app
from sqlalchemy.ext.declarative import declarative_base

MODEL_BASE = declarative_base()

LOG = logging.getLogger(__name__)


def create_engine(connection, idle_timeout=3600, max_pool_size=10, max_overflow=10,
                  pool_timeout=30, encoding='UTF-8', debug=False):
    """
    A function which represents create a database connection engine
    """
    db_url = make_url(connection)

    _init_engine_arguments = {'pool_recycle': idle_timeout,
                              'pool_size': max_pool_size,
                              'max_overflow': max_overflow,
                              'pool_timeout': pool_timeout,
                              'encoding': encoding,
                              'echo': debug}

    engine = sqlalchemy.create_engine(db_url, **_init_engine_arguments)
    return engine


class DbEngine(object):
    """
    A class which represents database connection engine.This class is a singleton class.

    .. attribute:: engine
        SQLAlchemy engine instance
    .. attribute:: session_maker
        SQLAlchemy session instance
    """
    def __init__(self, db_url=None, idle_timeout=3600, max_pool_size=10,
                 max_overflow=0, pool_timeout=30, encoding='UTF-8', debug=False):
        self._engine = create_engine(db_url,
                                     idle_timeout,
                                     max_pool_size,
                                     max_overflow,
                                     pool_timeout,
                                     encoding,
                                     debug)
        self._session_maker = sessionmaker(bind=self._engine)

    def get_engine(self):
        return self._engine

    def get_session(self, autocommit=True, expire_on_commit=False):
        return self._session_maker(autocommit=autocommit,
                                   expire_on_commit=expire_on_commit)

    @classmethod
    def get_instance(cls):
        """
        Get a instance of DBEngine
        :return: DBEngine instance
        """
        conn_url = app.config.get("SQLALCHEMY_DATABASE_URI")
        LOG.info('----Current database connection url is %s' % conn_url)
        return cls(conn_url)
