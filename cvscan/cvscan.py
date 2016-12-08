#!/usr/bin/env python
"""

Main program

"""

import converter 
import annotations_parser 
import details_parser 

class Resume:
  def __init__(self, file_path):
    self.file_path = file_path
    self.convert()
  def convert(self):
    # add functions to convert other formats to text
    if self.file_path.find(".pdf") != -1:
      self.resume_text = converter.pdf_to_txt(self.file_path)
    if self.resume_text is not '':
      self.fetch_all_details()
  def fetch_all_details(self):
    self.URLs = annotations_parser.fetch_pdf_urls(self.file_path)
    self.email = details_parser.fetch_email(self.resume_text)
    self.phone_numbers = details_parser.fetch_phone(self.resume_text)
    self.address = details_parser.fetch_address(self.resume_text)
    # TODO: Add more fetch here
  def show_raw_details(self):
    print '==================================================================='
    print '\nFile path:'
    print '-------------------------------------------------------------------'
    print self.file_path
    print '==================================================================='
    print '\nResume Text'
    print '-------------------------------------------------------------------'
    print self.resume_text
    print '==================================================================='
    print '\nURLs'
    print '-------------------------------------------------------------------'
    print self.URLs
    print '==================================================================='
    print '\nPhone numbers'
    print '-------------------------------------------------------------------'
    print self.phone_numbers
    print '==================================================================='
    print '\nEmails'
    print '-------------------------------------------------------------------'
    print self.email
    print '==================================================================='
    print '\nAddress'
    print '-------------------------------------------------------------------'
    print self.address
    print '==================================================================='
    print '-------------------------------------------------------------------'
    print '==================================================================='

# Will be made interactive at a later point of the development.
resume_name = raw_input('Enter Resume name to use:')
# resume_name = 'lakshmanaram'
file_name = '../data/input/'+resume_name+'.pdf'


resume = Resume(file_name)
resume.show_raw_details()