#! /usr/bin/env python
from setuptools import setup

descr = '''Parser for Pubmed Open-Access Subset XML Dataset'''

if __name__ == "__main__":
    setup(
        name='pubmed_parser',
        version='0.1.dev',
        description='Python parser for PubMed open source data',
        long_description=open('README.md').read(),
        url='https://github.com/titipata/pubmed_parser',
        author='Titipat Achakulvisut',
        author_email='titipata@u.northwestern.edu',
        license='(c) 2015 Titipat Achakulvisut, Daniel E. Acuna',
        keywords='pubmed parser',
        install_requires=['pandas', 'lxml', 'unidecode', 'nltk'],
        packages=['pubmed_parser'],
    )
