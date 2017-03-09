#!/usr/bin/env python
"""

A python script to get all job positions from an xls file.

"""
from openpyxl import load_workbook
import pickle

if __name__ == '__main__':
  wb = load_workbook('positions.xlsx')
  ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
  jobs = {}
  job_titles = ws.__getitem__("A")
  job_categories = ws.__getitem__("D")
  for title,category in zip(job_titles[1:],job_categories[1:]):
    if title.value:
      jobs[title.value.lower()] = category.value.lower()

  with open('positions','wb') as fp:
    pickle.dump(jobs,fp)
