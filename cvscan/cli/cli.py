# -*- encoding: utf-8 -*-
"""
Cvscan command line tool
"""

import click
import pprint

from cvscan import Cvscan
from cvscan import data_operations as do

# Disable the warning that Click displays (as of Click version 5.0) when users
# use unicode_literals in Python 2.
# See http://click.pocoo.org/dev/python3/#unicode-literals for more details.
click.disable_unicode_literals_warning = True

@click.group()
def main():
    """Cvscan command line tool."""
    pass

@main.command()
@click.option('--name', '-n', help='Parse resume')
def parse(name):
  """

  Parse resume
  Params: name Type: string
  Usage: cvscan parse --name <name>
  to parse file: ~/cvscan/<name>.pdf
  
  """
  resume = Cvscan(name)
  resume.parse()
  pprint.pprint(resume.show(), width=1)

@main.command()
@click.option('--org','-o',help='Explicitly add/remove an organization')
@click.option('--skill','-s',help='Add/Remove a skill')
@click.option('--job','-j',help='For adding a job: -j <job:category>')
def add(org,skill,job):
  """

  Add data to be considered
  Params: 
  org Type: string
  skill Type: string
  job Type: String (comma separated - job,category)
  Usage:
  For adding organization:
  cvscan add --org <org_name>
  For adding skill:
  cvscan add --skill <skill>
  For adding job:
  cvscan add --job <job,category>
  The above can be combined together also. Eg:
  cvscan add -o <org_name> -s <skill> is also valid

  """
  if org:
    do.add_organizations([org])
  if skill:
    do.add_skills([skill])
  if job:
    try:
      job = job.split(':')
      job = {job[0]:job[1]}
      do.add_jobs(job)
    except Exception:
      print "Something wnet wrong: " + Exception


@main.command()
@click.option('--org','-o',help='Explicitly add/remove an organization')
@click.option('--skill','-s',help='Add/Remove a skill')
@click.option('--job','-j',help='For removing a job -j <job>')
def remove(org,skill,job):
  """

  Remove data from consideration
  Params: 
  org Type: string
  skill Type: string
  job Type: String
  Usage:
  For adding organization:
  cvscan remove --org <org_name>
  For adding skill:
  cvscan remove --skill <skill>
  For adding job:
  cvscan remove --job <job>
  The above can be combined together also. Eg:
  cvscan remove -o <org_name> -s <skill> -j <job> is also valid

  """
  if org:
    do.remove_organizations([org])
  if skill:
    do.remove_skills([skill])
  if job:
    do.remove_jobs([job])
