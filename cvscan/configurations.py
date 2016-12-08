#!/usr/bin/env python
"""

Configurations file

"""

import re

# Regular expressinos used
regex_bullet = r"\(cid:\d{0,2}\)"
regex_email = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
def get_regex_phone(i,j,n):
  # regex explanation in order: 
  # optional braces open
  # optional +
  # one to three digit optional international code
  # optional braces close
  # optional whitespace separator
  # i digits
  # optional whitespace separator
  # j digits
  # optional whitespace separator
  # n-i-j digits
  return r"\(?(\+)?(\d{1,3})?\)?[\s-]{0,1}?(\d{"+str(i)+"})[\s\.-]{0,1}(\d{"+str(j)+"})[\s\.-]{0,1}(\d{"+str(n-i-j)+"})"
  
# there should be 1 non digit, followed by a whitespace
# then pin and trailing whitespace. 
# This is to avoid phone numbers being read as pincodes
regex_pincode = r"[^\d][\s\.\-](\d{6})[\s\.]"