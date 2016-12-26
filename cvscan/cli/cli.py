# -*- encoding: utf-8 -*-
"""
Cvscan command line tool
"""

import click
import pprint

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
  pprint.pprint(resume.show(), width=1)

# @click.group()
# def skill_operations:
#     """Operations on skills"""
#     pass

# @skill_operations.command()
# @click.option('--skill',default='',help="Enter skill to remove")
# def remove_skill(skill):
#   if skill:
#     with open(dirpath.PKGPATH + '/data/skills/skills','rb') as fp:
#       skills = pickle.load(fp)
#     if skill not in skills:
#       print "%s is not present in skills" % skill
#     else:
#       skills.remove(skill)
