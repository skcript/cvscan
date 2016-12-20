#!/usr/bin/env python
"""

Utility functions that uses language processing to extract useful information

"""
import pickle
import logging
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

    with open(dirpath.PKGPATH + '/data/skills/skills','rb') as fp:
        skills = pickle.load(fp)

    skill_set = []
    for skill in skills:
        stem_skill = skill.split()
        for word in skill:
            stem_skill.append(stemmer.stem(word))

        stem_skill = ' '.join(stem_skill)

        if skill.lower() in cleaned_resume:
            skill_set.append(skill)

    return skill_set
