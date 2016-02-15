import click

from unitedindread.config import read_db
import unitedindread.db as db
import unitedindread.listener as listener


@click.command()
@click.option('--connect', '-c')
def init(connect):
    db.init(connect)


@click.command()
@click.argument('users', nargs=-1)
def listen(users):
    listener.run(users)


@click.group()
def users():
    pass


@click.command(name='list')
@click.option('--tracked', '-t', is_flag=True)
def list_users(tracked):
    conf, err = read_db()
    with db.session(conf) as s:
        for u in s.query(db.User):
            if tracked and not u.is_tracking:
                continue
            click.echo('{team} {name}'.format(team=u.team,
                                              name=u.screen_name))


@click.command(name='add')
@click.option('--team', '-t', prompt=True)
@click.argument('users', nargs=-1)
def add_user(team, users):
    if len(team) != 3:
        raise IOError()
    conf, err = read_db()
    with db.session(conf) as s:
        for u in users:
            twit_user = listener.get_api().get_user(u)
            if not twit_user:
                continue
            db_user = listener.get_user(s, twit_user)
            db_user.team = team
            db_user.is_tracking = True
            s.merge(db_user)
            click.echo('Added {name}'.format(name=db_user.screen_name))


@click.group()
@click.version_option()
def main():
    pass

main.add_command(init)
main.add_command(listen)
users.add_command(add_user)
users.add_command(list_users)
main.add_command(users)

if __name__ == '__main__':
    main()
