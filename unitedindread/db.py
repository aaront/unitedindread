from contextlib import contextmanager

from sqlalchemy import create_engine, Column, ForeignKey, String, Integer, BigInteger, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from unitedindread.config import read_db

Base = declarative_base()

Session = sessionmaker()


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    screen_name = Column(String)
    is_tracking = Column(Boolean)


class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime)
    text = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    author_id = Column(BigInteger, ForeignKey('users.id'))
    author = relationship('User', foreign_keys=[author_id])
    retweets = Column(Integer)
    is_reply = Column(Boolean)


def _connect(database=None, user=None, password=None, host=None, port=None, config_path=None):
    if database is None:
        conf, cfg_path = read_db(config_path)
        if conf is None:
            raise IOError('Couldn\'t read config file in "{0}"'.format(cfg_path))
        database, user, password = conf['database'], conf['user'], conf['password']
        host, port = conf['host'], conf['port']
    if not host:
        host = 'localhost'
    if not port:
        port = 5432
    return create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))


@contextmanager
def session(database=None, user=None, password=None, host=None, port=None, config_path=None):
    Session.configure(bind=_connect(database, user, password, host, port, config_path))
    curr_session = Session()
    try:
        yield curr_session
    except:
        curr_session.rollback()
        raise
    finally:
        curr_session.close()


def init(database=None, user=None, password=None, host=None, port=None):
    Base.metadata.create_all(_connect(database, user, password, host, port))
