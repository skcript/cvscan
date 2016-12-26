#!/usr/bin/env python
"""

Main program

"""

import converter
import annotations_parser
import details_parser
import language_parser

import dirpath
import configurations

class Cvscan():
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

        if self.raw_text is not '':
            self.parse()
        else:
            raise ValueError("Error parsing resume.")

    def parse(self):
        self.URLs = annotations_parser.fetch_pdf_urls(self.path)
        self.emails = details_parser.fetch_email(self.raw_text)
        self.phone_numbers = details_parser.fetch_phone(self.raw_text)
        self.address = details_parser.fetch_address(self.raw_text)
        self.experience = details_parser.calculate_experience(self.raw_text)
        self.skills = language_parser.clean_resume(self.raw_text)

    # TODO: Add more fetch here
    def show(self):
        return {
            "experience" : self.experience,
            "address" : self.address,
            "phone_numbers" : self.phone_numbers,
            "emails" : self.emails,
            "urls" : self.URLs,
            "skills" : self.skills
        }