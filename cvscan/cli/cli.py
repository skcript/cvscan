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

  Parse resume\n
  Params: name Type: string\n
  Usage: cvscan parse --name <name>\n
  to parse file: ~/cvscan/<name>.pdf
  
  """
  resume = Cvscan(name)
  resume.parse()
  pprint.pprint(resume.show(), width=1)


@main.command()
@click.option('--org','-o',help='Explicitly add organizations')
@click.option('--skill','-s',help='Add skills')
@click.option('--job','-j',help='For adding jobs: -j <job:category>')
@click.option('--qual','-q',help="Add qualifications")
@click.option('--extra','-e',help = "Add Extra information")
def add(org,skill,job,qual,extra):
  """

  Add data to be considered\n
  Params: \n
  org Type: comma separated string\n
  skill Type: comma separated string\n
  job Type: comma separated string (comma separated - job:category)\n
  qual Type: comma separated string\n
  Usage:\n
  For adding organization:\n
  cvscan add --org <org_name,org_name,...>\n
  For adding skill:\n
  cvscan add --skill <skill,skill,...>\n
  For adding job:\n
  cvscan add --job <job:category,job:category,...>\n
  For adding qualification:\n
  cvscan add --qual <degree,degree,..>\n
  punctuations before the first and after the last alphabet are excluded\n
  For adding extra information:\n
  cvscan add --extra <extra,extra>\n
  The above can be combined together also. Eg:\n
  cvscan add -o <org_name,org_name,..> -s <skill,skill,..> is also valid

  """
  if org:
    do.add_organizations(org.split(','))
  if skill:
    do.add_skills(skill.split(','))
  if job:
    jobs = {}
    for _job in job.split(','):
      try:
        _job = _job.split(':')
        jobs[_job[0]] = _job[1]
      except Exception:
        print "Something wnet wrong: " + Exception
    do.add_jobs(jobs)
  if qual:
    do.add_qualifications(qual.split(','))
  if extra:
    do.add_extra(extra.split(','))

@main.command()
@click.option('--org','-o',help='Explicitly remove organizations')
@click.option('--skill','-s',help='Remove skills')
@click.option('--job','-j',help='For removing jobs -j <job>')
@click.option('--qual','-q',help="Remove qualifications")
@click.option('--extra','-e',help = "Remove Extra information")
def remove(org,skill,job,qual,extra):
  """

  Remove data from consideration\n
  Params:\n
  org Type: comma separated string\n
  skill Type: comma separated string\n  
  job Type: comma separated string\n
  qual Type: comma separated string\n
  Usage:\n   
  For removing organization:\n
  cvscan remove --org <org_name,org_name,..>\n
  For removing skill:\n
  cvscan remove --skill <skill,skill,..>\n
  For removing job:\n
  cvscan remove --job <job,job,..>\n
  For removing qualification:\n
  cvscan remove -q <degree,degree,..>\n
  punctuations before the first and after the last alphabet are excluded\n
  For removing extra information:\n
  cvscan remove -e <extra,extra>\n
  The above can be combined together also. Eg:\n
  cvscan remove -o <org_name,org_name,..> -s <skill,skill,..> -j <job>
  is also valid

  """
  if org:
    do.remove_organizations(org.split(','))
  if skill:
    do.remove_skills(skill.split(','))
  if job:
    do.remove_jobs(job.split(','))
  if qual:
    do.remove_qualifications(qual.split(','))
  if extra:
    do.remove_extra(extra.split(','))