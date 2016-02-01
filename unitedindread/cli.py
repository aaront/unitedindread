import click

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
@click.version_option()
def main():
    pass

main.add_command(init)
main.add_command(listen)

if __name__ == '__main__':
    main()
