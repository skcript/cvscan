#!/usr/bin/env python
"""

A utility to fetch details from the txt format of the resume

"""
import re
import pickle
import logging
from datetime import date
import configurations as regex

import dirpath

logging.basicConfig(level=logging.DEBUG)

"""

Utility function that fetches emails in the resume.
Params: resume_text type: string
returns: list of emails

"""
def fetch_email(resume_text):
  try:
    regular_expression = re.compile(regex.email, re.IGNORECASE)
    emails = []
    result = re.search(regular_expression, resume_text)
    while result:
      emails.append(result.group())
      resume_text = resume_text[result.end():]
      result = re.search(regular_expression, resume_text)
    return emails
  except Exception, exception_instance:
    logging.error('Issue parsing email: ' + str(exception_instance))
    return []


"""

Utility function that fetches phone number in the resume.
Params: resume_text type: string
returns: phone number type:string

"""
def fetch_phone(resume_text):
  try:
    regular_expression = re.compile(regex.get_phone(3, 3, 10), re.IGNORECASE)
    result = re.search(regular_expression, resume_text)
    phone = ''
    if result:
      result = result.group()
      for part in result:
        if part:
          phone += part
    if phone is '':
      for i in range(1, 10):
        for j in range(1, 10-i):
          regular_expression =re.compile(regex.get_phone(i, j, 10), re.IGNORECASE)
          result = re.search(regular_expression, resume_text)
          if result:
            result = result.groups()
            for part in result:
              if part:
                phone += part
          if phone is not '':
            return phone
    return phone
  except Exception, exception_instance:
    logging.error('Issue parsing phone number: ' + resume_text +
      str(exception_instance))
    return None


"""

Utility function that fetches address in the resume.
Params: resume_text type: string
returns: address type:dictionary keys:district, state, pincode

"""
def fetch_address(resume_text):
  pincode_input_path = dirpath.PKGPATH + '/data/address/pincodes'
  address_input_path = dirpath.PKGPATH + '/data/address/pincode-district-state'
  states_input = dirpath.PKGPATH + '/data/address/states'
  district_state_input = dirpath.PKGPATH + '/data/address/district-states'
  pincodes = set()
  states = set()
  district_states = {}
  address = {}
  result_address = {}
  initial_resume_text = resume_text

  with open(pincode_input_path, 'rb') as fp:
    pincodes = pickle.load(fp)
  with open(address_input_path, 'rb') as fp:
    address = pickle.load(fp)

  regular_expression = re.compile(regex.pincode)
  regex_result = re.search(regular_expression, resume_text)
  while regex_result:
    useful_resume_text = resume_text[:regex_result.start()].lower()
    pincode_tuple = regex_result.group()
    pincode = ''
    for i in pincode_tuple:
      if (i <= '9') and (i >= '0'):
        pincode += str(i)
    if pincode in pincodes:
      result_address['pincode'] = pincode
      result_address['state'] = address[pincode]['state'].title()
      result_address['district'] = address[pincode]['district'].title()
      return result_address

    result_address.clear()
    resume_text = resume_text[regex_result.end():]
    regex_result = re.search(regular_expression, resume_text)

  resume_text = initial_resume_text.lower()

  with open(states_input, 'rb') as fp:
    states = pickle.load(fp)
  with open(district_state_input, 'rb') as fp:
    district_states = pickle.load(fp)

  # Check if the input is a separate word in resume_text
  def if_separate_word(pos, word):
    if (pos != 0) and resume_text[pos-1].isalpha():
      return False
    final_pos = pos+len(word)
    if ( final_pos !=len(resume_text)) and resume_text[final_pos].isalpha():
      return False
    return True

  result_state = ''
  state_pos = len(resume_text)
  result_district = ''
  district_pos = len(resume_text)
  for state in states:
    pos = resume_text.find(state)
    if (pos != -1) and(pos < state_pos) and if_separate_word(pos, state):
      state_pos = pos
      result_state = state
  for district in district_states.keys():
    pos = resume_text.find(district)
    if (pos != -1) and (pos < district_pos) and if_separate_word(pos, district):
      district_pos = pos
      result_district = district
  if (result_state is '') and (result_district is not ''):
    result_state = district_states[result_district]

  result_address['pincode'] = ''
  result_address['district'] = result_district.title()
  result_address['state'] = result_state.title()
  return result_address


"""

Utility Function that calculates experience in the resume text
params: resume_text type:string
returns: experience type:int

"""
def calculate_experience(resume_text):
  #
  def get_month_index(month):
    month_dict = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    return month_dict[month.lower()]

  try:
    experience = 0
    start_month = -1
    start_year = -1
    end_month = -1
    end_year = -1
    regular_expression = re.compile(regex.date_range, re.IGNORECASE)
    regex_result = re.search(regular_expression, resume_text)
    while regex_result:
      date_range = regex_result.group()
      year_regex = re.compile(regex.year)
      year_result = re.search(year_regex, date_range)
      if (start_year == -1) or (int(year_result.group()) <= start_year):
        start_year = int(year_result.group())
        month_regex = re.compile(regex.months_short, re.IGNORECASE)
        month_result = re.search(month_regex, date_range)
        if month_result:
          current_month = get_month_index(month_result.group())
          if (start_month == -1) or (current_month < start_month):
            start_month = current_month
      if date_range.lower().find('present') != -1:
        end_month = date.today().month # current month
        end_year = date.today().year # current year
      else:
        year_result = re.search(year_regex, date_range[year_result.end():])
        if (end_year == -1) or (int(year_result.group()) >= end_year):
          end_year = int(year_result.group())
          month_regex = re.compile(regex.months_short, re.IGNORECASE)
          month_result = re.search(month_regex, date_range)
          if month_result:
            current_month = get_month_index(month_result.group())
            if (end_month == -1) or (current_month > end_month):
              end_month = current_month
      resume_text = resume_text[regex_result.end():]
      regex_result = re.search(regular_expression, resume_text)

    return end_year - start_year  # Use the obtained month attribute
  except Exception, exception_instance:
    logging.error('Issue calculating experience: '+str(exception_instance))
    return None


"""

Utility function that fetches Job Position from the resume.
Params: cleaned_resume Type: string
returns: job_positions Type:List

"""
def fetch_jobs(cleaned_resume):
  positions_path = dirpath.PKGPATH + '/data/job_positions/positions'
  with open(positions_path, 'rb') as fp:
    jobs = pickle.load(fp)

  job_positions = []
  positions = []
  for job in jobs.keys():
    job_regex = r'[^a-zA-Z]'+job+r'[^a-zA-Z]'
    regular_expression = re.compile(job_regex, re.IGNORECASE)
    regex_result = re.search(regular_expression, cleaned_resume)
    if regex_result:
      positions.append(regex_result.start())
      job_positions.append(job.capitalize())
  job_positions = [job for (pos, job) in sorted(zip(positions, job_positions))]

  # For finding the most frequent job category
  hash_jobs = {}
  for job in job_positions:
    if jobs[job.lower()] in hash_jobs.keys():
      hash_jobs[jobs[job.lower()]] += 1
    else:
      hash_jobs[jobs[job.lower()]] = 1

  # To avoid the "Other" category and 'Student' category from
  # becoming the most frequent one.
  if 'Student' in hash_jobs.keys():
    hash_jobs['Student'] = 0
  hash_jobs['Other'] = -1

  return (job_positions, max(hash_jobs, key=hash_jobs.get).capitalize())


"""

Utility function that fetches the skills from resume
Params: cleaned_resume Type: string
returns: skill_set Type: List

"""
def fetch_skills(cleaned_resume):
  with open(dirpath.PKGPATH + '/data/skills/skills', 'rb') as fp:
    skills = pickle.load(fp)

  skill_set = []
  for skill in skills:
    skill = ' '+skill+' '
    if skill.lower() in cleaned_resume:
      skill_set.append(skill)
  return skill_set


"""

Utility function that fetches degree and degree-info from the resume.
Params: resume_text Type: string
returns:
degree Type: List of strings
info Type: List of strings

"""
def fetch_qualifications(resume_text):
  degree_path = dirpath.PKGPATH + '/data/qualifications/degree'
  with open(degree_path, 'rb') as fp:
    qualifications = pickle.load(fp)

  degree = []
  info = []
  for qualification in qualifications:
    qual_regex = r'[^a-zA-Z]'+qualification+r'[^a-zA-Z]'
    regular_expression = re.compile(qual_regex, re.IGNORECASE)
    regex_result = re.search(regular_expression, resume_text)
    while regex_result:
      degree.append(qualification)
      resume_text = resume_text[regex_result.end():]
      lines = [line.rstrip().lstrip()
      for line in resume_text.split('\n') if line.rstrip().lstrip()]
      if lines:
        info.append(lines[0])
      regex_result = re.search(regular_expression, resume_text)
  return degree, info


"""

Utility function that fetches extra information from the resume.
Params: resume_text Type: string
returns: extra_information Type: List of strings

"""
def fetch_extra(resume_text):
  with open(dirpath.PKGPATH + '/data/extra/extra', 'rb') as fp:
    extra = pickle.load(fp)

  extra_information = []
  for info in extra:
    extra_regex = r'[^a-zA-Z]'+info+r'[^a-zA-Z]'
    regular_expression = re.compile(extra_regex, re.IGNORECASE)
    regex_result = re.search(regular_expression, resume_text)
    while regex_result:
      extra_information.append(info)
      resume_text = resume_text[regex_result.end():]
      regex_result = re.search(regular_expression, resume_text)
  return extra_information
