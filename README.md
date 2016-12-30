# cvscan
Your not so typical resume parser
Instructions
========
Follow these to have a sneak peek of what's going on  
1. git clone https://github.com/skcript/cvscan.git  
2. cd cvscan  
3. python setup.py install  
4. Place the sample resume in the ~/cvscan folder  and enter the file name  
or enter relative path  
Eg: ~/cvpath/data/sample/a.pdf is parsed by
```bash
cvscan parse --name data/sample/a
```

Data Manipulations
===============
## Skills
Note: Skills are case-sensitive unlike Jobs and Organizations
### add
```
cvscan add -s "C,C++,R,Java"
```
### remove
```
cvscan remove --skill "C,C++"
```

## Jobs
### add
Adding  
1. contributor Job-category: Programmer  
2. Android Programmer Job-category: Developer

```
cvscan add -j "contributor:Programmer,android Programmer:Developer"
```
### remove
Removing  
1. contributor  
2. Android Programmer  
```
cvscan remove --job "contributor,Android Programmer"
```

## Organizations
### add
```
cvscan add --org "Skcript"
```
### remove
```
cvscan remove -o "Skcript"
```

## Qualifications
Note:  
* Qualifications are case-sensitive.
* Puntuations before the first and after the last alphabet should be excluded

### add
```
cvscan add -q "B.S,B.Tech,B.Arch"
```
### remove
```
cvscan remove --qual "B.Arch"
```

## Extra Information
### add
```
cvscan add -e "machine learning,artificial intelligence"
```
### remove
```
cvscan remove --extra "machine learning,artificial intelligence"
```

File Descriptions
============
## class Cvscan
```
cvscan = Cvscan(name,path)
```
#### Extract
Convert the input file to raw_text and calls parse class method
```
cvscan.extract()
```
#### Display extracted text
```
cvscan.show()
```
### Attributes
| Attributes          | Function |
|---------------------|-----------|
|path                 | Stores the path of the resume |
|raw_text             | Stores the resume as raw text |
|URLs                 | Stores all the URLs from the resume |
|name                 | Applicant's name |
|emails               | Applicant's email |
|Phone number         | Applicant's contact number |
|address              | Applicant's address |
|experience           | Applicant's experience in years |
|cleaned_resume       | Raw text after removing english stopwords |
|skills               | Applicant's skillset |
|qualifications       | Applicant's qualifications |
|degree_info          | Info about qualification |
|job_positions        | Applicant's jobs |
|category             | Applicant's Job category |
|current_employers    | Organization applicant is working in |
|employers            | All organizations applicant has worked in |
|extra_info           | Extra information about the applicant|
<!--
## configurations.py
Contains the regular expressions used throughout the project
## converter.py
Contains methods to convert resume from input format to raw text
#### pdf_to_text
Uses pdfminer library to fetch raw text from the resume. Special characters and bullets in the resume are replaced with a newline character.  
This formatted text from the resume is returned.
 -->
