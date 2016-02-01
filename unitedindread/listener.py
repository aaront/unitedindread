import click
import tweepy

from unitedindread import db
from unitedindread.config import read_twitter, read_db


class DreadListener(tweepy.StreamListener):
    def __init__(self, api, db):
        self.api = api
        self.db = db
        super(tweepy.StreamListener, self).__init__()

    def on_status(self, status):
        with db.session(self.db) as session:
            if hasattr(status, 'retweeted_status'):
                add_retweet(session, status.user, status.retweeted_status)
                return
            add_get_tweet(session, status)
        try:
            click.echo('"{}" --{}'.format(status.text.encode('utf-8'),
                                          status.user.screen_name.encode('utf-8')))
        except:
            pass

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True

    def on_timeout(self):
        print('Timeout...')
        return True


def get_user(session, user):
    u = session.query(db.User).filter_by(id=user.id).one_or_none()
    if not user:
        u = db.User(id=user.id, screen_name=user.screen_name.encode('utf-8'))
    return u


def add_get_tweet(session, status):
    lng = None
    lat = None
    if status.coordinates is not None:
        coords = status.coordinates.coordinates
        lng = coords[0]
        lat = coords[1]
    tweet = session.query(db.Tweet).filter_by(id=status.id).one_or_none()
    if not tweet:
        tweet = db.Tweet(id=status.id, user=get_user(session, status.user), created_at=status.created_at,
                         text=status.text.encode('utf-8'), lat=lat, lng=lng)
        session.add(tweet)
    return tweet


def add_retweet(session, user, status):
    retweet = session.query(db.Retweet).filter_by(user_id=user.id, tweet_id=status.id).one_or_none()
    if retweet:
        retweet.count += 1
    else:
        retweet = db.Retweet(user=get_user(session, user), tweet=add_get_tweet(session, status), count=1)
    session.merge(retweet)


def get_user_id(api, user):
    u = api.get_user(user)
    return u.id_str


def get_api():
    twitter_config, cfg_path = read_twitter()
    if twitter_config is None:
        raise IOError('Couldn\'t read config file in "{0}"'.format(cfg_path))
    auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
    auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
    return tweepy.API(auth)


def run(users, async=False):
    api = get_api()
    conf, err = read_db()
    stream = tweepy.Stream(api.auth, DreadListener(api, conf))
    follow = [get_user_id(api, u) for u in users]
    stream.filter(follow=follow, languages=['en'], async=async)
