#!/usr/bin/env python
"""

Main program

"""

from get_txt import pdf_to_txt
from fetch_urls import fetch_pdf_urls
from fetch_details import fetch_email

# Will be made interactive at a later point of the development.
resume_name = raw_input('Enter Resume name to use:')
file_name = '../data/input/'+resume_name+'.pdf'
pdf_txt = pdf_to_txt(file_name)
print pdf_txt

links = fetch_pdf_urls(file_name)
for link in links:
  print link
  
print "\n\nEmail:"
email = fetch_email(pdf_txt)
print email