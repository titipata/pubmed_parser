---
title: 'Pubmed Parser: A Python Parser for Pubmed Open-Access XML Subset and MEDLINE XML Dataset'
tags:
  - Python
  - MEDLINE
  - Pubmed
  - Biomedical corpus
  - Natural Language Processing
authors:
  - name: Titipat Achakulvisut
    affiliation: 1
  - name: Daniel E. Acuna
    affiliation: 2
  - name: Ted Cybulski
    affiliation: 3
  - name: Kevin Henner
    affiliation: 4
  - name: Konrad Kording
    affiliation: 1
affiliations:
  - name: University of Pennsylvania
    index: 1
  - name: Syracuse University
    index: 2
  - name: Northwestern University
    index: 3
  - name: University of Washington
    index: 4

date: 15 December 2019
bibliography: paper.bib
---

# Summary

Biomedical publications are increasing exponetially in the recent years. Due to the availability of such large-scale corpus, researchers can mine the text and meta-data from such exploding of biomedical text. Examples of application are ranged from predicting of novel drug-drug interaction, classifying biomedical text data, targeted search engine made for specified oncological profile, or automatic learning of biomedical ontology. Python has become one of the datascience tool that researchers use for building machine learning model and deep learning model to analyze text data.

Pubmed Parser is built as an additional tool for parsing open biomedical text data from MEDLINE dataset and Pubmed Open-Access data using Python directly. It is built to parse incoming XML and HTML format to dictionary or JSON format suitable to future process. The implemented functions can be scaled easily using parallel functionality using [PySpark](https://spark.apache.org/). This allow users to parse the most recently available corpus and customize for their need.

Pubmed Parser has already been used in published work including [@achakulvisut2019claim; @vseva2019vist; @miller2017automated; @shahri2019propheno; @galea2018sub; @abdeddaim2018mesh]. It is also been used in multiple biomedical and natural language class projects and blog posts due to the ease of implemented functionalities.


# Acknowledgements

Titipat Achakulvisut was supportyed by the Royal Thai Government Scholarship grant #50AC002. Daniel E. Acuna is supported by National Science Foundation #XXXX.

# References