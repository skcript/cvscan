#!/usr/bin/env python
"""

A utility to fetch details from the txt format of the resume

"""
import re


"""

Utility function that fetches emails in the resume.
Params: resume_text type: string
returns: list of emails

"""
def fetch_email(resume_text):
  try:
    regular_expression = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}", re.IGNORECASE)
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
