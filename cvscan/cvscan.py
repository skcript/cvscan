#!/usr/bin/env python
"""

Main program

"""

from get_txt import pdf_to_txt
from fetch_urls import fetch_pdf_urls

# Will be made interactive at a later point of the development.
file_name = '../data/input/lakshmanaram.pdf'
pdf_txt = pdf_to_txt(file_name)
print pdf_txt

links = fetch_pdf_urls(file_name)
for link in links:
  print link
  