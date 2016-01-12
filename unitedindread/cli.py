import click

import unitedindread.db as db
import unitedindread.listener as listener


@click.command()
@click.option('--database', '-d')
@click.option('--user', '-u')
@click.option('--password', '-p')
@click.option('--host', '-h')
@click.option('--port', '-p')
def init(database, user, password, host, port):
    db.init(database, user, password, host, port)


@click.command()
@click.argument('users', nargs=-1)
def listen(users):
    listener.run(users)


@click.group()
@click.version_option()
def main():
    pass

main.add_command(init)
main.add_command(listen)

if __name__ == '__main__':
    main()
