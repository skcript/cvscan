#!/usr/bin/env python
"""

Main program

"""

from get_txt import pdf_to_txt

# Will be made interactive at a later point of the development.
file_name = '../data/input/lakshmanaram.pdf'
pdf_txt = pdf_to_txt(file_name)
print pdf_txt