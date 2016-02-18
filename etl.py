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


def exec_sql_query(query, params):
    pass


def get_sql_servers():
    cmd = SQLCMD + " -L"
    cmd_result = subprocess.check_output(cmd)
    if cmd_result:
        clean_result = ([line.strip().decode('utf-8')
                         for line in cmd_result.splitlines()
                         if len(line.strip())])

        # First line of the result is a silly 'Server:' text
        servers = clean_result[1:]
        return servers


def get_databases(server):
    with open('sql/list_db.sql', 'r') as fin:
        query = fin.read()
    cmd = SQLCMD + ' -h-1 -E -S {0} -Q "{1}"'.format(server, query)
    cmd_result = subprocess.check_output(cmd)
    if cmd_result:
        return [d.strip().decode('utf-8')
                for d in cmd_result.splitlines()
                if len(d.strip())]


def get_sql_server_info():
    return {s: get_databases(s) for s in get_sql_servers()}


def show_sql_servers_info():
    click.echo('Listing SQL Servers, please wait...')
    servers = get_sql_server_info()
    click.echo('Available SQL Servers:\n')
    for i, server in enumerate(servers, start=1):
        click.echo('\t{0} - {1}'.format(i, server))
        for j, db in enumerate(servers[server], start=1):
            click.echo('\t\t{0} - {1}'.format(j, db))
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
@click.option('dbname', '--dbname', '-d',
              help='Name of the SQL Server database',
              default='big_data_dmst')
@click.option('list_info', '--list', '-l',
              help='List the available SQL Servers and Databases',
              is_flag=True, default=False)
@click.option('create_schema', '--create-schema', '-c',
              help='Only create the schema on the SQL Server',
              is_flag=True, default=False)
def load(server, dbname, list_info, create_schema):
    if list_info:
        show_sql_servers_info()

if __name__ == '__main__':
    if not SQLCMD:
        click.echo('Could not detect sqlcmd.exe, please check your PATH')
        sys.exit(errno.EEXIST)
    cli()
