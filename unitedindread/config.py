import os
try:
    import ConfigParser as configparser
except ImportError:
    import configparser


def _config(config_path):
    if not config_path:
        config_path = os.path.join(os.path.expanduser('~'), '.unitedindread.ini')
    conf = configparser.ConfigParser()
    conf.read(config_path)
    return conf, config_path


def read_db(config_path=None):
    conf, config_path = _config(config_path)
    try:
        return conf.get('db', 'url'), config_path
    except configparser.NoSectionError:
        return None, config_path
    except configparser.NoOptionError:
        return None, config_path


def save_db(database_url, config_path=None):
    conf, config_path = _config(config_path)
    if 'db' not in conf.sections():
        conf.add_section('db')
    conf.set('db', 'url', database_url if database_url else '')
    with open(config_path, 'w') as config_file:
        conf.write(config_file)


def read_twitter(config_path=None):
    conf, config_path = _config(config_path)
    try:
        consumer_key = conf.get('twitter', 'consumer_key')
        consumer_secret = conf.get('twitter', 'consumer_secret')
        access_token = conf.get('twitter', 'access_token')
        access_token_secret = conf.get('twitter', 'access_token_secret')

        return dict(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        ), config_path
    except configparser.NoSectionError:
        return None, config_path
    except configparser.NoOptionError:
        return None, config_path
