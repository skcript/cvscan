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
          self.resume_text = converter.pdf_to_txt(self.path)

        if self.resume_text is not '':
          self.parse()

    def parse(self):
        self.URLs = annotations_parser.fetch_pdf_urls(self.path)
        self.email = details_parser.fetch_email(self.resume_text)
        self.phone_numbers = details_parser.fetch_phone(self.resume_text)
        self.address = details_parser.fetch_address(self.resume_text)
        self.experience = details_parser.calculate_experience(self.resume_text)
        self.cleaned_resume = language_parser.clean_resume(self.resume_text)

    # TODO: Add more fetch here
    def show(self):
        print '==================================================================='
        print '\nFile path:'
        print '-------------------------------------------------------------------'
        print self.path
        print '==================================================================='
        print '\nResume Text'
        print '-------------------------------------------------------------------'
        print self.resume_text
        print '==================================================================='
        print '\nURLs'
        print '-------------------------------------------------------------------'
        print self.URLs
        print '==================================================================='
        print '\nPhone numbers'
        print '-------------------------------------------------------------------'
        print self.phone_numbers
        print '==================================================================='
        print '\nEmails'
        print '-------------------------------------------------------------------'
        print self.email
        print '==================================================================='
        print '\nAddress'
        print '-------------------------------------------------------------------'
        print self.address
        print '==================================================================='
        print '\nExperience'
        print '-------------------------------------------------------------------'
        print str(self.experience) + " years"
        print '==================================================================='
        print '\nSkills'
        print '-------------------------------------------------------------------'
        print self.cleaned_resume
        print '==================================================================='
        print '-------------------------------------------------------------------'
        print '==================================================================='

# def main():
#   # Will be made interactive at a later point of the development.
#   resume_name = raw_input('Enter Resume name to use:')
#   # resume_name = 'lakshmanaram'
#   file_name = DIRPATH + '/data/input/'+resume_name+'.pdf'
#   print(file_name)
#   resume = Cvscan(file_name)
#   resume.show_raw_details()
#
# if __name__ == "__main__":
#     main()
