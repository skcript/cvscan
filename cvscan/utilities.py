#!/usr/bin/env python
"""

Contains all the constants and utility functions used through out the project

"""

import pickle
import dirpath

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
