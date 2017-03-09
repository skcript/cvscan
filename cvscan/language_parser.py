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

import utilities

logging.basicConfig(level=logging.DEBUG)

"""

Utility function that cleans the resume_text.
Params: resume_text type: string
returns: cleaned text ready for processing

"""
def clean_resume(resume_text):

  cleaned_resume = []

  # replacing newlines and punctuations with space
  resume_text =resume_text.replace('\t', ' ').replace('\n', ' ')
  for punctuation in string.punctuation:
    resume_text = resume_text.replace(punctuation, ' ')
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

  # Custom grammar with NLTK
  # NP - Noun Phrase
  # NN - Noun
  # NNP - Proper Noun
  # V - Verb
  # JJ - Adjective

  # In a sentence that contains NN NNNP V NN NN JJ NN.
  # The noun-phrases fetched are:
  # NP: NN NNP
  # NP: NN NN
  # NP: NN

  # Ex, "Application Developer at Delta Force"
  # => ["Application Developer", "Delta Force"]

  grammar = r"""NP: {<NN|NNP>+}"""
  parser = nltk.RegexpParser(grammar)

  avoid_organizations = utilities.get_avoid_organizations()

  for sentence in tokenized_sentences:

    # tags all parts of speech in the tokenized sentences
    tagged_words = nltk.pos_tag(nltk.word_tokenize(sentence))

    # then chunks with customize grammar
    # np_chunks are instances of class nltk.tree.Tree
    np_chunks = parser.parse(tagged_words)
    noun_phrases = []

    for np_chunk in np_chunks:
      if isinstance(np_chunk, nltk.tree.Tree) and np_chunk.label() == 'NP':
        # if np_chunk is of grammer 'NP' then create a space seperated string of all leaves under the 'NP' tree
        noun_phrase = ""
        for (org, tag) in np_chunk.leaves():
          noun_phrase += org + ' '

        noun_phrases.append(noun_phrase.rstrip())

    # Using name entity chunker to get all the organizations
    chunks = nltk.ne_chunk(tagged_words)
    for chunk in chunks:
      if isinstance(chunk, nltk.tree.Tree) and chunk.label() == 'ORGANIZATION':
        (organization, tag) = chunk[0]

        # if organization is in the noun_phrase, it means that there is a high chance of noun_phrase containing the employer name
        # eg, Delta Force is added to organizations even if only Delta is recognized as an organization but Delta Force is a noun-phrase
        for noun_phrase in noun_phrases:
          if organization in noun_phrase and organization not in avoid_organizations:
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
def fetch_employers_util(resume_text, job_positions, organizations):
  current_employers = []
  employers = []
  for job in job_positions:
    job_regex = r'[^a-zA-Z]'+job+r'[^a-zA-Z]'
    regular_expression = re.compile(job_regex, re.IGNORECASE)
    temp_resume = resume_text
    regex_result = re.search(regular_expression, temp_resume)
    while regex_result:

      # start to end point to a line before and after the job positions line
      # along with the job line
      start = regex_result.start()
      end = regex_result.end()
      lines_front = utilities.LINES_FRONT
      lines_back = utilities.LINES_BACK
      while lines_front != 0 and start != 0:
        if temp_resume[start] == '.':
          lines_front -= 1
        start -= 1
      while lines_back != 0 and end < len(temp_resume):
        if temp_resume[end] == '.':
          lines_back -= 1
        end += 1

      # Read from temp_resume with start and end as positions
      line = temp_resume[start:end].lower()

      for org in organizations:
        if org.lower() in line and org.lower() not in job_positions:
          if 'present' in line:
            if org.capitalize() in employers:
              employers.remove(org.capitalize())
            if org.capitalize() not in current_employers:
              current_employers.append(org.capitalize())
          elif org.capitalize() not in employers:
            employers.append(org.capitalize())

      temp_resume = temp_resume[end:]
      regex_result = re.search(regular_expression, temp_resume)

  return (current_employers, employers)


"""

Utility function that fetches the employers from resume
Params: resume_text Type: String
        job_positions Type: List of Strings
returns: employers Type: List of string

"""
def fetch_employers(resume_text, job_positions):

  # Cleaning up the text.
  # 1. Initially convert all punctuations to '\n'
  # 2. Split the resume using '\n' and add non-empty lines to temp_resume
  # 3. join the temp_resume using dot-space

  for punctuation in string.punctuation:
    resume_text = resume_text.replace(punctuation, '\n')

  temp_resume = []
  for x in resume_text.split('\n'):
    # append only if there is text
    if x.rstrip():
      temp_resume.append(x)

  # joined with dot-space
  resume_text = '. '.join(temp_resume)

  current_employers = []
  employers = []

  cur_emps, emps = fetch_employers_util(resume_text, job_positions,
    utilities.get_organizations())

  current_employers.extend(cur_emps)
  employers.extend(emps)

  cur_emps, emps = fetch_employers_util(resume_text, job_positions,
    fetch_all_organizations(resume_text))

  current_employers.extend([emp for emp in cur_emps
    if emp not in current_employers])
  employers.extend([emp for emp in emps
    if emp not in employers])

  return current_employers, employers


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
      if hasattr(chunk, 'label'):# and chunk.label() == 'PERSON':
        chunk = chunk[0]
      (name, tag) = chunk
      if tag == 'NOUN':
        return name

  return "Applicant name couldn't be processed"
