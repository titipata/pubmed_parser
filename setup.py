#! /usr/bin/env python
from setuptools import setup

if __name__ == "__main__":
    setup(
        name='pubmed_parser',
        version='0.1',
        description='Python parser for Pubmed Open-Access Subset and MEDLINE XML repository',
        long_description=open('README.md').read(),
        url='https://github.com/titipata/pubmed_parser',
        author='Titipat Achakulvisut',
        author_email='my.titipat@gmail.com',
        license='(c) 2015 Titipat Achakulvisut, Daniel E. Acuna',
        install_requires=['lxml', 'unidecode', 'requests'],
        packages=['pubmed_parser'],
        package_data={
            'pubmed_parser.data': ['*.xml.gz', '*.nxml', '*.txt'],
        }
    )
