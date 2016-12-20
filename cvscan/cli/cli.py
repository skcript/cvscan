# -*- encoding: utf-8 -*-
"""
Cvscan command line tool
"""

import click

from cvscan import Cvscan

# Disable the warning that Click displays (as of Click version 5.0) when users
# use unicode_literals in Python 2.
# See http://click.pocoo.org/dev/python3/#unicode-literals for more details.
click.disable_unicode_literals_warning = True

@click.group()
def main():
    """Cvscan command line tool."""
    pass

@main.command()
@click.option('--name', '-n', help='Redis key to be watched')
def parse(name):
    """Watching Redis for key."""
    resume = Cvscan(name)
    resume.parse()
    resume.show()
