# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cvscan',
    version='0.0.1',
    description='Your not so typical resume parser',
    long_description=readme,
    author='Swaathi Kakarla',
    author_email='swaathi@skcript.com',
    url = 'https://github.com/skcript/cvscan',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'cvscan': ['data/*/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cvscan = cvscan.cli:main',
        ],
    },
    install_requires=(
    	['click']
    )
)
