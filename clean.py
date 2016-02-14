from xml.etree.cElementTree import iterparse
from os import path

import click

SCRIPT_DIR = path.dirname(path.realpath(__file__))

DATA_DIR = path.join(SCRIPT_DIR, 'data')
TEMP_DIR = path.join(SCRIPT_DIR, 'tmp')

xml_files = {}
xml_files['users'] = path.join(DATA_DIR, 'Users.xml')
xml_files['posts'] = path.join(DATA_DIR, 'Posts.xml')
xml_files['tags'] = path.join(DATA_DIR, 'Tags.xml')
xml_files['comments'] = path.join(DATA_DIR, 'Comments.xml')
xml_files['votes'] = path.join(DATA_DIR, 'Votes.xml')
xml_files['badges'] = path.join(DATA_DIR, 'Badges.xml')


@click.command()
def clean():
    pass


if __name__ == '__main__':
    clean()
