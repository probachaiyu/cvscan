#!/usr/bin/env python
"""

Script to process the data from locdetails_15feb16_4.csv downloaded from 
https://data.gov.in/catalog/locality-based-pincode

"""

import pickle
import csv
import re

pincodes = set()
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
      # district_name = set()
      # district_name.add(row['DistrictName'].lower())
      district_name = row['DistrictName'].lower()
      sub_district_name = set()
      # if row['locality_detail1'].lower() is not 'na':
      #   sub_district_name.add(row['locality_detail1'].lower())
      address[row['Pincode']] = {'state': state_name, 'district':district_name}#,
      # 'sub_district' :sub_district_name }
      # address_keywords = set()
      # address_keywords.add(row['\xef\xbb\xbfStateName'])
      # address_keywords.add(row['DistrictName'])
      # address_keywords.add(row['subdistname'])
      # address[row['Pincode']] = address_keywords
    # else:
      # address[row['Pincode']]['state'].add(row['\xef\xbb\xbfStateName'].lower())
      # address[row['Pincode']]['district'].add(row['DistrictName'].lower())
      # if row['locality_detail1'].lower() is not 'na':
      #   address[row['Pincode']]['sub_district'].add(row['locality_detail1'].lower())
      # address[row['Pincode']].add(row['\xef\xbb\xbfStateName'])
      # address[row['Pincode']].add(row['DistrictName'])
      # address[row['Pincode']].add(row['subdistname'])

# Store pincodes list in pincodes
with open('pincodes','wb') as fp:
  pickle.dump(pincodes,fp)

# Store address dictionaries
with open('pincode-district-state','wb') as fp:
  pickle.dump(address,fp)

    # regular_expression = re.compile(r"(\d{6})")
    # result = re.search(regular_expression,pincode)
    # if result:
    #   print (row['pincode'],row['Taluk'],row['Districtname'],row['statename'])
