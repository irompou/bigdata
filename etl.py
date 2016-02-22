from os import path
import sys
import errno
import subprocess

import click

from util import which

SCRIPT_DIR = path.dirname(path.realpath(__file__))
DATA_DIR = path.join(SCRIPT_DIR, 'data')
SQLCMD = which('SQLCMD.exe')
DEFAULT_DB_NAME = 'big_data_dmst'

CREATE_DB_QUERY = path.join(SCRIPT_DIR, r'sql\create_db.sql')
CREATE_SCHEMA_QUERY = path.join(SCRIPT_DIR, r'sql\create_tables.sql')
IMPORT_QUERY = path.join(SCRIPT_DIR, r'sql\import.sql')
LIST_DB_QUERY = path.join(SCRIPT_DIR, r'sql\list_db.sql')
DROP_DB_QUERY = path.join(SCRIPT_DIR, r'sql\drop_db.sql')


class ConnectionInfo(object):
    def __init__(self, server, db):
        self.server = server
        self.db = db


def exec_sql_query(server, db='', query_path=None, params=None):
    """ Executes the passed query file and returns results as a list """
    with open(query_path, 'r') as fin:
        query = fin.read()

    envargs = ''
    if params and len(params):
        envargs = ' '.join(['-v {0}="{1}"'.format(k, v)
                            for k, v in params.items()])

    if len(db):
        db = '-d ' + db

    cmd = SQLCMD + ' -h-1 -E -S {server} {db} {envargs} -Q "{query}"'
    cmd = cmd.format(server=server, db=db, envargs=envargs, query=query)
    cmd_result = subprocess.check_output(cmd)
    if cmd_result:
        return [d.strip().decode('utf-8')
                for d in cmd_result.splitlines()
                if len(d.strip())]


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
    return exec_sql_query(server=server, db='', query_path=LIST_DB_QUERY)


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


def create_database(server, db_name):
    click.echo('Creating database on {0}'.format(server))
    if exec_sql_query(server=server, query_path=CREATE_DB_QUERY,
                      params={'db_name': db_name}):
        click.echo('Database "{0}" created'.format(db_name))


def create_schema(server, db):
    click.echo('Creating schema on {0}/{1}'.format(server, db))
    if exec_sql_query(server=server, db=db, query_path=CREATE_SCHEMA_QUERY):
        click.echo('Schema on "{0}" created'.format(db))


def import_data_job(server, db, xml_path):
    click.echo('Importing data from {0} on {1}/{2}'.format(
        xml_path, server, db))
    if exec_sql_query(server=server, db=db,
                      query_path=IMPORT_QUERY, params={'xml_path': xml_path}):
        click.echo('Schema on "{0}" created'.format(db))


def destroy_db(server, db_name):
    click.echo('Dropping database {0} from {1}'.format(db_name, server))
    if exec_sql_query(server=server, db='', query_path=DROP_DB_QUERY,
                      params={'db_name': db_name}):
        click.echo('Database "{0}" was dropped'.format(db_name))


@click.group(chain=True, invoke_without_command=True)
@click.option('server', '--server', '-s',
              help='URL of the SQL Server',
              default='localhost')
@click.option('db', '--db', '-d',
              help='Name of the SQL Server database. '
                   'If the database is not found, it\'s created automaticaly',
              default=DEFAULT_DB_NAME)
@click.option('list_info', '--list', '-l',
              help='List the available SQL Servers and Databases',
              is_flag=True, default=False)
@click.pass_context
def cli(ctx, server, db, list_info):
    ctx.obj = ConnectionInfo(server, db)
    if list_info:
        show_sql_servers_info()


@cli.command()
@click.pass_obj
def init(conn):
    if conn.db not in get_databases(conn.server):
        create_database(conn.server, conn.db)
    create_schema(conn.server, conn.db)


@cli.command(name='import')
@click.argument('source', default=DATA_DIR)
@click.pass_obj
def import_cmd(conn, source):
    import_data_job(conn.server, conn.db, source)


@cli.command()
@click.pass_obj
def destroy(conn):
    destroy_db(conn.server, conn.db)


if __name__ == '__main__':
    if not SQLCMD:
        click.echo('Could not detect sqlcmd.exe, please check your PATH')
        sys.exit(errno.EEXIST)
    cli()
