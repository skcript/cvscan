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

not_alpha_numeric = r'[^a-zA-Z\d]'

# there should be 1 non digit, followed by a whitespace
# then pin and trailing whitespace. 
# This is to avoid phone numbers being read as pincodes
regex_pincode = r"[^\d]"+not_alpha_numeric+"(\d{6})"+not_alpha_numeric

months_short = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
months_long = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)(september)|(october)|(november)|(december)'
month = '('+months_short+months_long+')'
year = r'((20|19)(\d{2})|(\d{2}))'
start_date = month+not_alpha_numeric+r"?"+year
end_date = '(('+month+not_alpha_numeric+r"?"+year+')|(present))'+not_alpha_numeric
longer_year = r"((20|19)(\d{2}))"
year_range = longer_year+not_alpha_numeric+r"{1,3}"+longer_year
regex_date_range =  "("+start_date+not_alpha_numeric+r"{1,3}"+end_date+")|("+year_range+")"