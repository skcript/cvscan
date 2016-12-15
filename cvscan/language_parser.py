#!/usr/bin/env python
"""

Utility functions that uses language processing to extract useful information

"""
import pickle
import logging

logging.basicConfig(level=logging.DEBUG)

__author__ = 'lakshmanaram'
__license__ = 'http://opensource.org/licenses/MIT'
__email__ = 'lakshmanaram.n@gmail.com'
__maintainer__ = 'lakshmanaram'


"""

Utility function that cleans the resume_text.
Params: resume_text type: string
returns: cleaned text ready for processing

"""
def clean_text(resume_text):
  return resume_text