"""

Contains util functinos to add organizations to files 
explicit_organizations and avoid_organizations in the parent folder
which are used by fetch_employer module

"""

import pickle


"""

An Utility function to add organizations to the explicit_organizations file.
Params: orgs Type: List of String

"""
def add_organizations(orgs):
  with open(dirpath.PKGPATH + 'explicit_organizations') as fp:
    organizations = pickle.load(fp)
  with open(dirpath.PKGPATH + 'avoid_organizations') as fp:
    avoid_organizations = pickle.load(fp)
  for org in orgs:
    if org.lower().capitalize() not in organizations:
      organizations.append(org.lower().capitalize())
    if org.lower().capitalize() in avoid_organizations:
      avoid_organizations.remove(org.lower().capitalize())
  with open(dirpath.PKGPATH + 'explicit_organizations') as fp:
    pickle.dump(organizations, fp)
  with open(dirpath.PKGPATH + 'avoid_organizations') as fp:
    pickle.dump(avoid_organizations, fp)


"""

An Utility function to add organization to be avoided.
Params: orgs Type: List of String

"""
def remove_organizations(orgs):
  with open(dirpath.PKGPATH + 'explicit_organizations') as fp:
    organizations = pickle.load(fp)
  with open(dirpath.PKGPATH + 'avoid_organizations') as fp:
    avoid_organizations = pickle.load(fp)
  for org in orgs:
    if org.lower().capitalize() not in avoid_organizations:
      avoid_organizations.append(org.lower().capitalize())
    if org.lower().capitalize() in organizations:
      organizations.remove(org.lower().capitalize())
  with open(dirpath.PKGPATH + 'explicit_organizations') as fp:
    pickle.dump(organizations, fp)
  with open(dirpath.PKGPATH + 'avoid_organizations') as fp:
    pickle.dump(avoid_organizations, fp)
