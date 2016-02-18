import subprocess

import requests
import click

from os import path, makedirs

data_urls = {}
data_urls['stats'] = (r'https://archive.org/download/stackexchange/'
                      'stats.stackexchange.com.7z')
data_urls['dba'] = (r'https://archive.org/download/stackexchange/'
                    'dba.stackexchange.com.7z')
data_urls['datascience'] = (r'https://archive.org/download/stackexchange/'
                            'datascience.stackexchange.com.7z')

SCRIPT_DIR = path.dirname(path.realpath(__file__))

DATA_DIR = path.join(SCRIPT_DIR, 'data')
TEMP_DIR = path.join(SCRIPT_DIR, 'tmp')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', type=click.Path())
def extract(path):
    subprocess.call('7z.exe x ' + path + ' -y -o' + DATA_DIR)


@cli.command()
@click.option('url', '--url', '-u', help='URL to data file')
@click.option('data', '--data', '-d', type=click.Choice(data_urls.keys()))
@click.option('outfile', '--outfile', '-o', type=click.Path())
def download(url, data, outfile):
    if data:
        url = data_urls[data]
    if not outfile:
        file_from_url = url.split('/')[-1]
        outfile = path.join(TEMP_DIR, file_from_url)

    makedirs(TEMP_DIR, exist_ok=True)

    r = requests.get(url, stream=True)
    total_length = int(r.headers.get('content-length'))
    download = click.progressbar(r.iter_content(chunk_size=1024),
                                 label='Downloading data file',
                                 length=(total_length/1024) + 1)
    click.echo('Writing to {0}'.format(click.format_filename(outfile)))
    with download, open(outfile, 'wb') as fout:
        for chunk in download:
            if chunk:
                fout.write(chunk)
                fout.flush()
    click.echo(click.format_filename(outfile))

if __name__ == '__main__':
    cli()
