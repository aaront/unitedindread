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


@click.command(name='add')
@click.option('--team', '-t', prompt=True)
@click.argument('users', nargs=-1)
def add_user(team, users):
    if len(team) != 3:
        raise IOError()
    conf, err = read_db()
    with db.session(conf) as session:
        for u in users:
            user_obj = db.User()


@click.group()
@click.version_option()
def main():
    pass

main.add_command(init)
main.add_command(listen)
users.add_command(add_user)
main.add_command(users)

if __name__ == '__main__':
    main()
