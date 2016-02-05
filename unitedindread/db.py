from contextlib import contextmanager

from sqlalchemy import create_engine, Column, ForeignKey, String, Integer, BigInteger, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

from unitedindread.config import read_db

Base = declarative_base()

session_factory = sessionmaker()
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    screen_name = Column(String)
    is_tracking = Column(Boolean)
    team = Column(String(length=3))
    tweets = relationship('Tweet', backref='user')
    retweets = relationship('Retweet', backref='user')


class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.id'))
    created_at = Column(DateTime)
    text = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    retweets = relationship('Retweet', backref='tweet')


class Retweet(Base):
    __tablename__ = 'retweet'
    user_id = Column(BigInteger, ForeignKey('user.id'), primary_key=True)
    tweet_id = Column(BigInteger, ForeignKey('tweet.id'), primary_key=True)
    count = Column(Integer, default=1)


def _connect(connect_url=None, config_path=None):
    if connect_url is None:
        connect_url, cfg_path = read_db(config_path)
        if connect_url is None:
            raise IOError('Couldn\'t read config file in "{0}"'.format(cfg_path))
    return create_engine(connect_url)


@contextmanager
def session(connect_url=None, config_path=None):
    Session.configure(bind=_connect(connect_url, config_path))
    curr_session = Session()
    try:
        yield curr_session
        curr_session.commit()
    except:
        curr_session.rollback()
        raise
    finally:
        curr_session.close()


def init(connect_url=None):
    Base.metadata.create_all(_connect(connect_url))
