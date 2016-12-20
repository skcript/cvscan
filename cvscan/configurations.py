#!/usr/bin/env python
"""

Configurations file

"""

import re
import os

# Get environment variable or return default value
def get_env_var(var, default):
    try:
        env_var = os.environ[var]
        return env_var
    except:
        return default

def isfile(path):
    return os.path.isfile(path)

# Regular expressinos used
bullet = r"\(cid:\d{0,2}\)"
email = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
def get_phone(i,j,n):
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

not_alpha_numeric = r'[^a-zA-Z\d]'
number = r'\d+'

# there should be 1 non digit, followed by a whitespace
# then pin and trailing whitespace.
# This is to avoid phone numbers being read as pincodes
pincode = r"[^\d]"+not_alpha_numeric+"(\d{6})"+not_alpha_numeric

# For finding date ranges
months_short = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
months_long = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'
month = r'('+months_short+r'|'+months_long+r')'
year = r'((20|19)(\d{2})|(\d{2}))'
start_date = month+not_alpha_numeric+r"?"+year
end_date = r'(('+month+not_alpha_numeric+r"?"+year+r')|(present))'+not_alpha_numeric
longer_year = r"((20|19)(\d{2}))"
year_range = longer_year+not_alpha_numeric+r"{1,3}"+longer_year
date_range =  r"("+start_date+not_alpha_numeric+r"{1,3}"+end_date+r")|("+year_range+r")"
