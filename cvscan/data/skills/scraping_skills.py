#!/usr/bin/env python
"""

A python script to scrape all LinkedIN skills.

"""
from selenium import webdriver
from string import ascii_lowercase
import pickle
import logging

logging.basicConfig(level=logging.DEBUG)

"""

Utility function that scrapes all skills from that aprticular LinkedIN page.
params: selenium Webdriver, webpage URL
returns: list of skills in that page (strings)

"""
def fetch_all_skills_in_page(driver,path):
  driver.get(path)
  skills_in_page = []
  links_in_page = []
  elements_list = driver.find_elements_by_class_name('content')
  for element in elements_list:
    a_tag = element.find_element_by_tag_name('a')
    link = a_tag.get_attribute('href')
    if "https://www.linkedin.com/topic/" in link:
      skills_in_page.append(element.text)
    else:
      links_in_page.append(link)
  return skills_in_page,links_in_page

"""

Utility function that scrapes all skills from LinkedIN.
returns: list of skills (strings)

"""
def fetch_all_skills(links_to_check):
  driver = webdriver.Firefox()
  driver.get("https://www.linkedin.com/")
  skills = []
  while len(links_to_check) != 0:
    checking_links = links_to_check
    links_to_check = []
    for link in checking_links:
      skills_in_page,links_in_page = fetch_all_skills_in_page(driver,link)
      skills.extend(skills_in_page)
      links_to_check.extend(links_in_page)
  return skills

if __name__ == "__main__":
  links_to_check = ["https://www.linkedin.com/directory/topics-z/"]
  skills = []
  with open('skills','rb') as fp:
    skills = pickle.load(fp)
  # links_to_check = []
  # for c in ascii_lowercase:
  #   links_to_check.append('https://www.linkedin.com/directory/topics-'+c+'/')
  skills.extend(fetch_all_skills(links_to_check))
  with open('skills','wb') as fp:
    pickle.dump(skills,fp)
