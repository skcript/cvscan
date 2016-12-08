#!/usr/bin/env python
"""

A utility to fetch details from the txt format of the resume

"""
import re
import pickle
import logging

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
    regular_expression = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}",
                                    re.IGNORECASE)
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
    regular_expression = re.compile(r"\(?"  # open parenthesis
                                    r"(\+)?"
                                    r"(\d{1,3})?"  # International code
                                    r"\)?"  # close parenthesis
                                    r"[\s-]{0,1}?"  # separator
                                    r"(\d{3})"  # 3 digit exchange
                                    r"[\s\.-]{0,1}"  # separator 
                                    r"(\d{3})"  # 3 digit exchange
                                    r"[\s\.-]{0,1}"  # separator 
                                    r"(\d{4})",  # 4 digit local
                                    re.IGNORECASE)
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
          regular_expression = re.compile(r"\(?"  # open parenthesis
                                          r"(\+)?"
                                          r"(\d{1,3})?" # Area code
                                          r"\)?"  # close parenthesis
                                          r"[\s-]{0,1}?"  # separator
                                          r"(\d{"+str(i)+"})"
                                          r"[\s\.-]{0,1}"  # separator 
                                          r"(\d{"+str(j)+"})"
                                          r"[\s\.-]{0,1}"  # separator 
                                          r"(\d{"+str(10-i-j)+"})",
                                          re.IGNORECASE)
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
  pincodes = []
  address = {}
  with open(pincode_input_path, 'rb') as fp:
    pincodes = pickle.load(fp)
  with open(address_input_path,'rb') as fp:
    address = pickle.load(fp)

  logging.debug("Fetching pincodes from the resume test")
  initial_resume_text = resume_text

  # there should be 1 non digit, followed by a whitespace
  # then pin and trailing whitespace. 
  # This is to avoid phone numbers being read as pincodes
  regular_expression = re.compile(r"[^\d][\s\.\-](\d{6})[\s\.]")
  regex_result = re.search(regular_expression,resume_text)
  
  result_address = {}
  while regex_result:
    useful_resume_text = resume_text[:regex_result.start()].lower()
    pincode_tuple = regex_result.group()
    pincode = ''
    for i in pincode_tuple:
      if (i <= '9') and (i >= '0'):
        pincode += str(i)
    if pincode in pincodes:
      result_address['pincode'] = pincode
      result_address['state'] = address[pincode]['state']
      result_address['district'] = address[pincode]['district']
      # Getting valid list of states, districts and localitites to search
      # valid_districts = address[pincode]['district']
      # valid_localities = address[pincode]['sub_district']

      # for district in valid_districts:
      #   if useful_resume_text.find(district) != -1:
      #     result_address['district'] = district
      #     break

      # for locality in valid_localities:
      #   if useful_resume_text.find(locality) != -1:
      #     result_address['locality'] = locality
      #     break
      
      # if ('state' in result_address.keys()) or ('district' in result_address.keys()) or ('locality' in result_address.keys()):
      #   if 'state' not in result_address.keys():
      #     for state in address[pincode]['state']:
      #       result_address['state'] = state
      #   if 'district' not in result_address.keys():
      #     result_address['district'] = ''
      #   if 'locality' not in result_address.keys():
      #     result_address['locality'] = ''
      return result_address

    result_address.clear()
    resume_text = resume_text[regex_result.end():]
    regex_result = re.search(regular_expression,resume_text)

  logging.debug("Fetching states and districts from the resume test")
  resume_text = initial_resume_text.lower()

  states = set()
  districts = set()
  for record in address.values():
    states.add(record['state'])
    districts.add(record['district'])

  result_state = ''
  state_pos = len(resume_text)
  result_district = ''
  district_pos = len(resume_text)
  for state in states:
    pos = resume_text.find(state)
    if (pos != -1) and(pos < state_pos)and((pos == 0)or not resume_text[pos-1].isalpha())and((pos+len(state)==len(resume_text))or not resume_text[pos+len(state)].isalpha()):
      state_pos = pos
      result_state = state

  for district in districts:
    pos = resume_text.find(district)
    if (pos != -1) and(pos < district_pos)and((pos == 0)or not resume_text[pos-1].isalpha())and((pos+len(district)==len(resume_text))or not resume_text[pos+len(district)].isalpha()):
      district_pos = pos
      result_district = district

  

  result_address['pincode'] = ''
  result_address['district'] = result_district
  result_address['state'] = result_state
  return result_address