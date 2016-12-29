"""

Contains util functions for manipulating the data used by cvscan

"""

import pickle
import logging

import dirpath

logging.basicConfig(level=logging.DEBUG)

DATAPATH = dirpath.PKGPATH + '/data/'


"""

An Utility function to add organizations to the explicit_organizations file.
Params: orgs Type: List of String

"""
def add_organizations(orgs):
  with open(DATAPATH + 'organizations/explicit_organizations','rb') as fp:
    organizations = pickle.load(fp)
  with open(DATAPATH + 'organizations/avoid_organizations','rb') as fp:
    avoid_organizations = pickle.load(fp)
  logging.debug("explicit_organizations and avoid_organizations files loaded")

  for org in orgs:
    if org.lower().capitalize() not in organizations:
      organizations.append(org.lower().capitalize())
      logging.debug(org + "added to explicit_organizations")
    if org.lower().capitalize() in avoid_organizations:
      avoid_organizations.remove(org.lower().capitalize())
      logging.debug(org + "removed from avoid_organizations")
  
  with open(DATAPATH + 'organizations/explicit_organizations','wb') as fp:
    pickle.dump(organizations, fp)
  with open(DATAPATH + 'organizations/avoid_organizations','wb') as fp:
    pickle.dump(avoid_organizations, fp)
  logging.debug("explicit_organizations and avoid_organizations files written")


"""

An Utility function to add organization to be avoided.
Params: orgs Type: List of String

"""
def remove_organizations(orgs):
  with open(DATAPATH + 'organizations/explicit_organizations','rb') as fp:
    organizations = pickle.load(fp)
  with open(DATAPATH + 'organizations/avoid_organizations','rb') as fp:
    avoid_organizations = pickle.load(fp)
  logging.debug("explicit_organizations and avoid_organizations files loaded")

  for org in orgs:
    if org.lower().capitalize() not in avoid_organizations:
      avoid_organizations.append(org.lower().capitalize())
      logging.debug(org + "added to avoid_organizations")
    if org.lower().capitalize() in organizations:
      organizations.remove(org.lower().capitalize())
      logging.debug(org + "removed from explicit_organizations")

  with open(DATAPATH + 'organizations/explicit_organizations','wb') as fp:
    pickle.dump(organizations, fp)
  with open(DATAPATH + 'organizations/avoid_organizations','wb') as fp:
    pickle.dump(avoid_organizations, fp)
  logging.debug("explicit_organizations and avoid_organizations files written")


"""

An Utility function to add skills.
Params: skills_to_add Type: List of Strings

"""
def add_skills(skills_to_add):
  with open(DATAPATH +'skills/skills','rb') as fp:
    skills = pickle.load(fp)
  for skill in skills_to_add:
    if skill.lower() not in skills:
      skills.append(skill.lower())
  with open(DATAPATH +'skills/skills','wb') as fp:
    pickle.dump(skills,fp)
  

"""

An Utility function to remove skills.
Params: skills_to_remove Type: List of Strings

"""
def remove_skills(skills_to_remove):
  with open(DATAPATH +'skills/skills','rb') as fp:
    skills = pickle.load(fp)
  for skill in skills_to_remove:
    if skill.lower() in skills:
      skills.remove(skill.lower())
  with open(DATAPATH +'skills/skills','wb') as fp:
    pickle.dump(skills,fp)
