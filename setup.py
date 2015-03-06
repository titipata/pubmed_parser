#!/usr/bin/env python

from distutils.core import setup

setup(
    name='pubmed_parser',
    version='0.1.dev',
    description='Python parser for PubMed open source data',
    url='https://github.com/titipata/pubmed_parser',
    author='Titipat Achakulvisut',
    author_email='titipata@u.northwestern.edu',
    license='(c) 2015 Titipat Achakulvisut, Daniel E. Acuna',
    keywords='pubmed parser',
    install_requires=['pandas', 'lxml'],
)
