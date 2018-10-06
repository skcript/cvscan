#!/usr/bin/env python
"""

Contains all the constants and utility functions used through out the project

"""

import pickle
from . import dirpath

DATAPATH = dirpath.PKGPATH + '/data/'

# Constants
LINES_FRONT = 3
LINES_BACK = 3

# Methods
def get_avoid_organizations():
  with open(dirpath.PKGPATH +
    '/data/organizations/avoid_organizations') as fp:
    avoid_organizations = pickle.load(fp)
  return avoid_organizations

def get_organizations():
  with open(dirpath.PKGPATH +
    '/data/organizations/explicit_organizations') as fp:
    organizations = pickle.load(fp)
  return organizations


def get_degree():
  with open(DATAPATH + 'qualifications/degree', 'rb') as fp:
    degrees = pickle.load(fp)
  return degrees

def get_skills():
  with open(DATAPATH +'skills/skills','rb') as fp:
    skills = pickle.load(fp)
  return skills


def get_extra():
  with open(DATAPATH + 'extra/extra','rb') as fp:
    extra = pickle.load(fp)
  return extra

def get_qualifications():
  with open(DATAPATH + 'qualifications/degree','rb') as fp:
    qualifications = pickle.load(fp)
  return qualifications

def get_jobs():
  with open(DATAPATH +'job_positions/positions','rb') as fp:
    jobs = pickle.load(fp)
  return jobs