#!/usr/bin/env python
"""

Main program

"""

from . import converter
from . import annotations_parser
from . import details_parser as dp
from . import language_parser as lp

from . import dirpath
from . import configurations

class Cvscan():

    URLs = None
    name = None
    emails = None
    phone_numbers = None
    address = None
    experience = None
    cleaned_resume = None
    skills = None
    qualifications = None
    degree_info = None
    job_positions = None
    category = None
    current_employers = None
    employers = None
    extra_info = None

    def __init__(self, name, path = dirpath.RESUMEPATH):
        self.path = path + '/' + name + '.pdf'

        if self.exists():
            self.extract()
        else:
            raise OSError("There is no file found at " + self.path)

    def exists(self):
        return configurations.isfile(self.path)

    # Extracts raw text from resume
    # Currently only supports PDF
    def extract(self):
        # add functions to convert other formats to text
        if self.path.find(".pdf") != -1:
            self.raw_text = converter.pdf_to_txt(self.path)

        if self.raw_text is not '' and len(self.raw_text)>25:
            self.parse()
        else:
            print ("Error extracting resume text.")
            return


    def parse(self):
        self.URLs = annotations_parser.fetch_pdf_urls(self.path)
        self.name = lp.fetch_name(self.raw_text)
        self.departement = lp.fetch_zip(self.raw_text)
        #print "self.departement ",self.departement
        if not self.departement:
            self.ville  = lp.fetch_ville(self.raw_text)
        self.emails = dp.fetch_email(self.raw_text)
        self.phone_numbers = dp.fetch_phone(self.raw_text)
        self.address = dp.fetch_address(self.raw_text)
        self.experience = dp.calculate_experience(self.raw_text)
        self.cleaned_resume = lp.clean_resume(self.raw_text)
        self.skills = dp.fetch_skills(self.cleaned_resume)
        (self.qualifications,self.degree_info) = dp.fetch_qualifications(
            self.raw_text)
        self.job_positions, self.category = dp.fetch_jobs(self.cleaned_resume)
        self.current_employers,self.employers = lp.fetch_employers(
            self.raw_text,self.job_positions)
        self.extra_info = dp.fetch_extra(self.raw_text)

    # TODO: Add more fetch here
    def show(self):
        return {
            "name" : self.name,
            "experience" : self.experience,
            "address" : self.address,
            "phone_numbers" : self.phone_numbers,
            "emails" : self.emails,
            "urls" : self.URLs,
            "skills" : self.skills,
            "jobs" : self.job_positions,
            "job category" : self.category,
            "employers" : self.employers,
            "current_employers" : self.current_employers,
            "qualifications" : self.qualifications,
            "qualifications_info" : self.degree_info,
            "extra_info" : self.extra_info
        }
