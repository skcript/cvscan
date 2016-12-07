#!/usr/bin/env python
"""

A utility to fetch details from the txt format of the resume

"""
import re
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
def fetch_phone(string_to_search):
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
    result = re.search(regular_expression, string_to_search)
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
          result = re.search(regular_expression, string_to_search)
          if result:
            result = result.groups()
            for part in result:
              if part:
                phone += part
          if phone is not '':
            return phone
    return phone
  except Exception, exception_instance:
    logging.error('Issue parsing phone number: ' + string_to_search + 
      str(exception_instance))
    return None
