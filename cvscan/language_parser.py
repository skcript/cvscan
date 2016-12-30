#!/usr/bin/env python
"""

Utility functions that uses language processing to extract useful information

"""
import pickle
import logging
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

import dirpath

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
def clean_resume(resume_text):

  cleaned_resume = []

  # replacing newlines and punctuations with space
  resume_text =resume_text.replace('\t',' ').replace('\n',' ')
  for punctuation in string.punctuation:
    resume_text = resume_text.replace(punctuation,' ')
  resume_text = resume_text.split()

  # removing stop words and Stemming the remaining words in the resume
  stemmer = SnowballStemmer("english")
  for word in resume_text:
    if word not in stopwords.words('english') and not word.isdigit():
      cleaned_resume.append(word.lower())#stemmer.stem(word))

  cleaned_resume = ' '.join(cleaned_resume)
  return cleaned_resume


"""

Util function for fetch_employers module to get all the
organization names from the resume
Params: resume_text Type:String
Output: Set of all organizations Type: Set of strings

"""
def fetch_all_organizations(resume_text):
  organizations = set()
  tokenized_sentences = nltk.sent_tokenize(resume_text)
  grammar = r"""NP: {<NN|NNP>+}"""
  parser = nltk.RegexpParser(grammar)

  for sentence in tokenized_sentences:
    tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))

    np_chunks = parser.parse(tagged_words)
    noun_phrases = []
    for np_chunk in np_chunks:
      if isinstance(np_chunk,nltk.tree.Tree) and np_chunk.label() == 'NP':
        noun_phrase = ' '.join([org for (org,tag) in np_chunk.leaves()])
        noun_phrases.append(noun_phrase)
    # print noun_phrases

    chunks = nltk.ne_chunk(tagged_words)
    for chunk in chunks:
      if hasattr(chunk,'label') and chunk.label() == 'ORGANIZATION':
        (organization,tag) = chunk[0]
        for noun_phrase in noun_phrases:
          if organization in noun_phrase:
            organizations.add(noun_phrase.capitalize())

  return organizations


"""

Util function for fetch_employers module to get employers
All organizations found near any job position is regarded as an employer
Params: resume_text Type:String
        job_positions Type: List of Strings
        organizations Type: List of Strings
        priority Type: Boolean True/False
Output: current_employers Type: List of strings
        all_employers Type: List of strings

"""
def fetch_employers_util(resume_text, job_positions, organizations, priority):
  current_employers = []
  employers = []
  for job in job_positions:
    job_regex = r'[^a-zA-Z]'+job+r'[^a-zA-Z]'
    regular_expression = re.compile(job_regex, re.IGNORECASE)
    temp_resume = resume_text
    regex_result = re.search(regular_expression,temp_resume)
    while regex_result:
      # start to end point to a line before and after the job positions line
      # along with the job line
      start = regex_result.start()
      end = regex_result.end()
      lines_front = lines_back = 3
      while lines_front != 0 and start != 0:
        if temp_resume[start] == '.':
          lines_front -= 1
        start -= 1
      while lines_back != 0 and end < len(temp_resume):
        if temp_resume[end] == '.':
          lines_back -= 1
        end += 1
      line = temp_resume[start:end].lower()
      # print line
      for org in organizations:
        if org.lower() in line and org.lower() not in job_positions:
          if 'present' in line:
            # print org
            if org.capitalize() in employers:
              employers.remove(org.capitalize())
            if org.capitalize() not in current_employers:
              if priority:
                current_employers.insert(0,org.capitalize())
              else:
                current_employers.append(org.capitalize())
          elif org.capitalize() not in employers:
            if priority:
              employers.insert(0,org.capitalize())
            else:
              employers.append(org.capitalize())
      temp_resume = temp_resume[end:]
      regex_result = re.search(regular_expression,temp_resume)
  return (current_employers,employers)


"""

Utility function that fetches the employers from resume
Params: resume_text Type: String
        job_positions Type: List of Strings
returns: employers Type: List of string

"""
def fetch_employers(resume_text, job_positions):
  for punctuation in string.punctuation:
    resume_text = resume_text.replace(punctuation,'\n')
  resume_text = '. '.join([x for x in resume_text.split('\n')
    if len(x.rstrip().lstrip())!=0])
  with open(dirpath.PKGPATH +
    '/data/organizations/avoid_organizations') as fp:
    avoid_organizations = pickle.load(fp)

  current_employers = []
  employers = []
  organizations = [org for org in fetch_all_organizations(resume_text)
  if org not in avoid_organizations]
  cur_emps,emps = fetch_employers_util(resume_text, job_positions,
    organizations,False)
  current_employers.extend(cur_emps)
  employers.extend(emps)

  with open(dirpath.PKGPATH +
    '/data/organizations/explicit_organizations') as fp:
    organizations = pickle.load(fp)
  cur_emps,emps = fetch_employers_util(resume_text, job_positions,
    organizations,True)
  current_employers.extend([emp for emp in cur_emps
    if emp not in current_employers])
  employers.extend([emp for emp in emps
    if emp not in employers])

  return current_employers,employers


"""

Utility function that fetches the Person Name from resume
Params: resume_text Type: string
returns: name Type: string

Returns the first noun (tried Person entity but couldn't make it work)
found by tokenizing each sentence
If no such entities are found, returns "Applicant name couldn't be processed"

"""
def fetch_name(resume_text):
  tokenized_sentences = nltk.sent_tokenize(resume_text)
  for sentence in tokenized_sentences:
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence), tagset='universal')):
      if hasattr(chunk,'label'):# and chunk.label() == 'PERSON':
        chunk = chunk[0]
      (name,tag) = chunk
      if tag == 'NOUN':
        return name

  return "Applicant name couldn't be processed"
