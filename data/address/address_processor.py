#!/usr/bin/env python
"""

Script to process the data from locdetails_15feb16_4.csv downloaded from 
https://data.gov.in/catalog/locality-based-pincode

"""

import pickle
import csv
import re

pincodes = set()
district_state = {}
states = set()
address = {}

data_file = 'locdetails_15feb16_4.csv'
with open(data_file) as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    prev_size = len(pincodes)
    pincodes.add(row['Pincode'])
    cur_size = len(pincodes)
    if cur_size != prev_size:
      state_name = row['\xef\xbb\xbfStateName'].lower()
      district_name = row['DistrictName'].lower()
      sub_district_name = set()
      address[row['Pincode']] = {'state': state_name, 'district':district_name}
      states.add(state_name)
      district_state[district_name] = state_name

# Store pincodes list in pincodes
with open('pincodes','wb') as fp:
  pickle.dump(pincodes,fp)

# Store address dictionaries
with open('pincode-district-state','wb') as fp:
  pickle.dump(address,fp)

# Store distric-state dictionaries
with open('district-states','wb') as fp:
  pickle.dump(district_state,fp)

# Store states list
with open('states','wb') as fp:
  pickle.dump(states,fp)
