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
        database = conf.get('db', 'database')
        user = conf.get('db', 'user')
        password = conf.get('db', 'password')
        host = conf.get('db', 'host')
        port = conf.get('db', 'port')

        return dict(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        ), config_path
    except configparser.NoSectionError:
        return None, config_path
    except configparser.NoOptionError:
        return None, config_path


def save_db(database, user, password, host, port, config_path=None):
    conf, config_path = _config(config_path)
    if 'db' not in conf.sections():
        conf.add_section('db')
    conf.set('db', 'database', database if database else '')
    conf.set('db', 'user', user if user else '')
    conf.set('db', 'password', password if password else '')
    conf.set('db', 'host', host if host else '')
    conf.set('db', 'port', port if port else '')
    with open(config_path, 'w') as config_file:
        conf.write(config_file)


def read_twitter_api(config_path=None):
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
