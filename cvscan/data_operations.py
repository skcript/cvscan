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
Organization names aren't case-sensitive

"""
def add_organizations(orgs):
  with open(DATAPATH + 'organizations/explicit_organizations','rb') as fp:
    organizations = pickle.load(fp)
  with open(DATAPATH + 'organizations/avoid_organizations','rb') as fp:
    avoid_organizations = pickle.load(fp)
  logging.debug("explicit_organizations and avoid_organizations files loaded")

  for org in orgs:
    if org.capitalize() not in organizations:
      organizations.append(org.capitalize())
      logging.debug(org+" added to explicit_organizations")
    if org.capitalize() in avoid_organizations:
      avoid_organizations.remove(org.capitalize())
      logging.debug(org+" removed from avoid_organizations")

  with open(DATAPATH + 'organizations/explicit_organizations','wb') as fp:
    pickle.dump(organizations, fp)
  with open(DATAPATH + 'organizations/avoid_organizations','wb') as fp:
    pickle.dump(avoid_organizations, fp)
  logging.debug("explicit_organizations and avoid_organizations files written")


"""

An Utility function to add organization to be avoided.
Params: orgs Type: List of String
Organization names aren't case-sensitive

"""
def remove_organizations(orgs):
  with open(DATAPATH + 'organizations/explicit_organizations','rb') as fp:
    organizations = pickle.load(fp)
  with open(DATAPATH + 'organizations/avoid_organizations','rb') as fp:
    avoid_organizations = pickle.load(fp)
  logging.debug("explicit_organizations and avoid_organizations files loaded")

  for org in orgs:
    if org.capitalize() not in avoid_organizations:
      avoid_organizations.append(org.capitalize())
      logging.debug(org + " added to avoid_organizations")
    if org.capitalize() in organizations:
      organizations.remove(org.capitalize())
      logging.debug(org + " removed from explicit_organizations")

  with open(DATAPATH + 'organizations/explicit_organizations','wb') as fp:
    pickle.dump(organizations, fp)
  with open(DATAPATH + 'organizations/avoid_organizations','wb') as fp:
    pickle.dump(avoid_organizations, fp)
  logging.debug("explicit_organizations and avoid_organizations files written")


"""

An Utility function to add skills.
Params: skills_to_add Type: List of Strings
skills to add are case sensitive

"""
def add_skills(skills_to_add):
  with open(DATAPATH +'skills/skills','rb') as fp:
    skills = pickle.load(fp)
  logging.debug("skills file loaded")

  for skill in skills_to_add:
    if skill not in skills:
      skills.append(skill)
      logging.debug(skill + " has been added to skills")

  with open(DATAPATH +'skills/skills','wb') as fp:
    pickle.dump(skills,fp)
  logging.debug("updated skills")

"""

An Utility function to remove skills.
Params: skills_to_remove Type: List of Strings
skills to remove are case sensitive.

"""
def remove_skills(skills_to_remove):
  with open(DATAPATH +'skills/skills','rb') as fp:
    skills = pickle.load(fp)
  logging.debug("skills file loaded")

  for skill in skills_to_remove:
    if skill in skills:
      skills.remove(skill)
      logging.debug(skill + " has been removed from skills")
    else:
      logging.warning(skill + " not found. Check the case and Try again.")

  with open(DATAPATH +'skills/skills','wb') as fp:
    pickle.dump(skills,fp)
  logging.debug("updated skills file")


"""

An Utility function to add job and job category to positions data.
Params: jobs_to_add Type: dictionary
Keys: job string   Values: Respective job category string
jobs and the job categories aren't case sensitive

"""
def add_jobs(jobs_to_add):
  with open(DATAPATH +'job_positions/positions','rb') as fp:
    jobs = pickle.load(fp)
  logging.debug("positions file loaded")

  for job,category in jobs_to_add.iteritems():
    if job.lower() in jobs.keys() and category.lower() != jobs[job]:
      logging.debug("Job category of "+job+" has been changed from "+
        jobs[job]+" to "+category)
      jobs[job] = category
    elif job.lower() not in jobs.keys():
      jobs[job.lower()] = category.lower()
      logging.debug("added "+job+" - "+category)

  with open(DATAPATH +'job_positions/positions','wb') as fp:
    pickle.dump(jobs,fp)
  logging.debug("updated positions file")



"""

An Utility function to remove job from positions data.
Params: jobs_to_remove Type: List of Strings
jobs aren't case sensitive

"""
def remove_jobs(jobs_to_remove):
  with open(DATAPATH +'job_positions/positions','rb') as fp:
    jobs = pickle.load(fp)
  logging.debug("positions file loaded")

  for job in jobs_to_remove:
    if job.lower() in jobs.keys():
      del jobs[job.lower()]
      logging.debug("deleted "+job+" from the positions file")

  with open(DATAPATH +'job_positions/positions','wb') as fp:
    pickle.dump(jobs,fp)
  logging.debug("updated positions file")


"""

An Utility function to add qualification to the degree file.
Params: qualifications Type: List of String
Qualifications are case-sensitive.
Care should be taken with the punctuations.
Exclude punctuations before the first alphabet and after the last alphabet.

"""
def add_qualifications(quals):
  with open(DATAPATH + 'qualifications/degree','rb') as fp:
    qualifications = pickle.load(fp)
  logging.debug("degree file loaded")

  for qual in quals:
    if qual not in qualifications:
      qualifications.append(qual)
      logging.debug(qual + " added to qualifications")

  with open(DATAPATH + 'qualifications/degree','wb') as fp:
    pickle.dump(qualifications, fp)
  logging.debug("degree file written")


"""

An Utility function to remove qualification from the degree file.
Params: qualifications Type: List of String
Qualifications are case-sensitive.
Care should be taken with the punctuations.
Exclude punctuations before the first alphabet and after the last alphabet.

"""
def remove_qualifications(quals):
  with open(DATAPATH + 'qualifications/degree','rb') as fp:
    qualifications = pickle.load(fp)
  logging.debug("degree file loaded")

  for qual in quals:
    if qual in qualifications:
      qualifications.remove(qual)
      logging.debug(qual + " removed from qualifications")

  with open(DATAPATH + 'qualifications/degree','wb') as fp:
    pickle.dump(qualifications, fp)
  logging.debug("degree file written")


"""

An Utility function to add extra information to the extra file.
Params: extra_info Type: List of String
extra_info are case-sensitive.

"""
def add_extra(extra_info):
  with open(DATAPATH + 'extra/extra','rb') as fp:
    extra = pickle.load(fp)
  logging.debug("extra file loaded")

  for e in extra_info:
    if e not in extra:
      extra.append(e)
      logging.debug(e + " added to extra information")

  with open(DATAPATH + 'extra/extra','wb') as fp:
    pickle.dump(extra, fp)
  logging.debug("extra file written")


"""

An Utility function to remove extra information from the extra file.
Params: extra_info Type: List of String
Extra informations are case-sensitive.

"""
def remove_extra(extra_info):
  with open(DATAPATH + 'extra/extra','rb') as fp:
    extra = pickle.load(fp)
  logging.debug("extra file loaded")

  for e in extra_info:
    if e in extra:
      extra.remove(e)
      logging.debug(e + " removed from extra information")

  with open(DATAPATH + 'extra/extra','wb') as fp:
    pickle.dump(extra, fp)
  logging.debug("extra file written")
