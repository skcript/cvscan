#!/usr/bin/env python
"""

Utility functions that uses language processing to extract useful information

"""
import pickle
import logging
import nltk
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
  resume_text =resume_text.replace('\t',' ').replace('\n',' ').replace('.',' ')
  resume_text = resume_text.replace(',',' ').replace('/',' ').replace('(',' ')
  resume_text = resume_text.replace(')',' ').replace('|',' ').replace('!',' ')
  resume_text = resume_text.split()

  # removing stop words and Stemming the remaining words in the resume
  stemmer = SnowballStemmer("english")
  for word in resume_text:
    if word not in stopwords.words('english') and not word.isdigit():
      cleaned_resume.append(word.lower())#stemmer.stem(word))
          
  cleaned_resume = ' '.join(cleaned_resume)
  return cleaned_resume


"""
TODO: move this function to the details parser as stem isn't used

Utility function that fetches the skills from resume
Params: cleaned_resume Type: string
returns: skill_set Type: List

"""
def fetch_skills(cleaned_resume):
  with open(dirpath.PKGPATH + '/data/skills/skills','rb') as fp:
    skills = pickle.load(fp)

  skill_set = []
  for skill in skills:
    # stem_skill = skill.split()
    # for word in skill:
    #   stem_skill.append(stemmer.stem(word))
    # stem_skill = ' '.join(stem_skill)
    skill = ' '+skill+' '
    if skill.lower() in cleaned_resume:
      skill_set.append(skill)
  return skill_set


"""

Utility function that fetches the current employer from resume
Params: resume_text Type: string
returns: current_employer Type: string

"""
def fetch_employer(cleaned_resume, resume_text, job_positions):
  organizations = set()
  resume_text = resume_text.replace('-','\n').replace('|','\n')
  resume_text = '. '.join([x for x in resume_text.split('\n') 
    if len(x.rstrip().lstrip())!=0])
  print resume_text
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
            organizations.add(noun_phrase)

  for job in job_positions:
    job_regex = r'[^a-zA-Z]'+job+r'[^a-zA-Z]'
    regular_expression = re.compile(job_regex)
    regex_result = re.search(regular_expression,cleaned_resume)
    while regex_result:
      positions.append(regex_result.start())
      job_positions.append(job)
      regex_result = re.search(regular_expression,cleaned_resume)

  # for org in organization:
  
  # check if organization and job positions go together
  
  return organizations
  # if any of this organization is beside a job position, assume it as an emplyer

  # return current_employer


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