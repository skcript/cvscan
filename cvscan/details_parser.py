#!/usr/bin/env python
"""

A utility to fetch details from the txt format of the resume

"""
import re
import pickle
import logging
import configurations

logging.basicConfig(level=logging.DEBUG)

__author__ = 'lakshmanaram'
__license__ = 'http://opensource.org/licenses/MIT'
__email__ = 'lakshmanaram.n@gmail.com'
__maintainer__ = 'lakshmanaram'


"""

Utility function that fetches emails in the resume.
Params: resume_text type: string
returns: list of emails

"""
def fetch_email(resume_text):
  try:
    regular_expression = re.compile(configurations.regex_email,re.IGNORECASE)
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
    regular_expression = re.compile(configurations.get_regex_phone(3,3,10),re.IGNORECASE)
    result = re.search(regular_expression, resume_text)
    phone = ''
    if result:
      result = result.groups()
      for part in result:
        if part:
          phone += part
    if phone is '':
      for i in range(1,10):
        for j in range(1,10-i):
          regular_expression = re.compile(configurations.get_regex_phone(i,j,10),re.IGNORECASE)
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
returns: address type:dictionary keys:district,state,pincode

"""
def fetch_address(resume_text):
  pincode_input_path = '../data/address/pincodes'
  address_input_path = '../data/address/pincode-district-state'
  states_input = '../data/address/states'
  district_state_input = '../data/address/district-states'
  pincodes = set()
  states = set()
  district_states = {}
  address = {}
  result_address = {}
  initial_resume_text = resume_text
  logging.debug("Fetching pincodes from the resume test")

  with open(pincode_input_path, 'rb') as fp:
    pincodes = pickle.load(fp)
  with open(address_input_path,'rb') as fp:
    address = pickle.load(fp)

  regular_expression = re.compile(configurations.regex_pincode)
  regex_result = re.search(regular_expression,resume_text)
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
    regex_result = re.search(regular_expression,resume_text)

  logging.debug("Fetching states and districts from the resume test")
  resume_text = initial_resume_text.lower()

  with open(states_input,'rb') as fp:
    states = pickle.load(fp)
  with open(district_state_input,'rb') as fp:
    district_states = pickle.load(fp)
  
  # Check if the input is a separate word in resume_text
  def if_separate_word(pos,word):
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
    if (pos != -1) and(pos < state_pos) and if_separate_word(pos,state):
      state_pos = pos
      result_state = state
  for district in district_states.keys():
    pos = resume_text.find(district)
    if (pos != -1) and (pos < district_pos) and if_separate_word(pos,district):
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
  