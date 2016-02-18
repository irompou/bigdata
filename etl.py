import os
import sys
import errno
import subprocess

import click

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
TEMP_DIR = os.path.join(SCRIPT_DIR, 'tmp')

xml_files = {}
xml_files['users'] = os.path.join(DATA_DIR, 'Users.xml')
xml_files['posts'] = os.path.join(DATA_DIR, 'Posts.xml')
xml_files['tags'] = os.path.join(DATA_DIR, 'Tags.xml')
xml_files['comments'] = os.path.join(DATA_DIR, 'Comments.xml')
xml_files['votes'] = os.path.join(DATA_DIR, 'Votes.xml')
xml_files['badges'] = os.path.join(DATA_DIR, 'Badges.xml')


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


SQLCMD = which('SQLCMD.exe')


def get_sql_servers():
    result = subprocess.check_output(SQLCMD + " -L")
    if result:
        clean_result = ([line.strip().decode('utf-8')
                         for line in result.splitlines() if len(line.strip())])
        # First line of the result is a silly 'Server:' text
        server_list = clean_result[1:]
        return sorted(server_list)


def show_sql_servers():
    click.echo('Listing SQL Servers, please wait...')
    servers = get_sql_servers()
    click.echo('Available SQL Servers:\n')
    for i, s in enumerate(servers, start=1):
        click.echo('\t{0} - {1}'.format(i, s))
        return


@click.group()
def cli():
    pass


@cli.command()
def extract():
    pass


@cli.command()
def transform():
    pass


@cli.command()
@click.option('server', '--server', '-s',
              help='URL of the SQL Server',
              default='localhost')
@click.option('list_servers', '--list-servers', '-l',
              help='List the available SQL Servers',
              is_flag=True, default=False)
@click.option('dbname', '--dbname', '-d',
              help='Name of the SQL Server database',
              default='big_data_dmst')
def load(server, dbname, list_servers):
    if list_servers:
        show_sql_servers()


if __name__ == '__main__':
    if not SQLCMD:
        click.echo('Could not detect sqlcmd.exe, please check your PATH')
        sys.exit(errno.EEXIST)
    cli()
