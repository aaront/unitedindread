import click
import tweepy

from unitedindread import db
from unitedindread.config import read_twitter_api


class DreadListener(tweepy.StreamListener):
    def __init__(self, api, session):
        self.api = api
        self.session = session
        super(tweepy.StreamListener, self).__init__()

    def on_status(self, status):
        user = get_user(status.user)
        if hasattr(status, 'retweeted_status'):
            status = status.retweeted_status
        author = get_user(status.user)
        text = status.text.encode('utf-8')
        tweet = self.session.query(db.Tweet).filter_by(id=status.id).one_or_none()
        if not tweet:
            tweet = db.Tweet(id=status.id, created_at=status.created_at, text=text,
                             author=author, is_reply=(status.in_reply_to_status_id is not None))
            if status.coordinates is not None:
                coords = status.coordinates.coordinates
                tweet.lng = coords[0]
                tweet.lat = coords[1]
        if user.id != author.id:
            if tweet.retweets is None:
                tweet.retweets = 0
            tweet.retweets += 1
        self.session.merge(author)
        self.session.merge(tweet)
        self.session.commit()
        try:
            click.echo('"{}" --{}'.format(text, status.user.screen_name.encode('utf-8')))
        except:
            pass

    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return True

    def on_timeout(self):
        print('Timeout...')
        return True


def get_user(user):
    return db.User(id=user.id, screen_name=user.screen_name)


def get_user_id(api, user):
    u = api.get_user(user)
    return u.id_str


def get_api():
    twitter_config, cfg_path = read_twitter_api()
    if twitter_config is None:
        raise IOError('Couldn\'t read config file in "{0}"'.format(cfg_path))
    auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
    auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])
    return tweepy.API(auth)


def run(users):
    api = get_api()
    with db.session() as session:
        stream = tweepy.Stream(api.auth, DreadListener(api, session))
        follow = [get_user_id(api, u) for u in users]
        stream.filter(follow=follow, languages=['en'])
