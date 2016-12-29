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
