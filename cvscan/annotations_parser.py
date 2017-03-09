#!/usr/bin/env python
"""

A utility to fetch urls from the resume

"""

import logging

# for fetching URLs from pdf
from pdfminer.pdfpage import PDFPage

logging.basicConfig(level=logging.DEBUG)

"""

Utility Function to fetch URLs from pdf.
Params: file_name type: string
returns: list of URLs

"""
def fetch_pdf_urls(file_name):
  try:
    links = []
    file_pointer = open(file_name,'rb')

    # Setting up pdf document
    pdf_pages = PDFPage.get_pages(file_pointer)

    # fetches URLs
    for page in pdf_pages:
      if 'Annots' in page.attrs.keys():
        link_object_list = page.attrs['Annots']
        # Due to implementation of pdfminer the link_object_list can either
        # be the list directly or a PDF Object reference
        if type(link_object_list) is not list:
          link_object_list = link_object_list.resolve()
        for link_object in link_object_list:
          if type(link_object) is not dict:
            link_object = link_object.resolve()
          if link_object['A']['URI']:
            links.append(link_object['A']['URI'])
    file_pointer.close()
    return links

  except Exception, exception_instance:
    logging.error('Error while fetching URLs : '+str(exception_instance))
    return ''
