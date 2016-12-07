#!/usr/bin/env python
"""

A utility to fetch urls from the resume

"""

import logging

# for fetching URLs from pdf
from pdfminer.pdfpage import PDFPage

logging.basicConfig(level=logging.DEBUG)

__author__ = 'lakshmanaram'
__license__ = 'http://opensource.org/licenses/MIT'
__email__ = 'lakshmanaram.n@gmail.com'
__maintainer__ = 'lakshmanaram'


"""

Utility Function to fetch URLs from pdf.
Params: file_name type: string
returns: list of URLs

"""
def fetch_pdf_urls(file_name):
  try:
    links = []
    file_pointer = open(file_name,'rb')

    logging.debug("Fetching URLs from pdf")

    # Setting up pdf document
    pdf_pages = PDFPage.get_pages(file_pointer)

    # fetches URLs
    for page in pdf_pages:
      link_object_list = page.attrs['Annots']
      for link_object in link_object_list.resolve():
        links.append(link_object.resolve()['A']['URI'])
    file_pointer.close()
    return links

  except Exception, exception_instance:
    logging.error('Error while fetching URLs : '+str(exception_instance))
    return ''
