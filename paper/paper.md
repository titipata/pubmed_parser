---
title: 'Pubmed Parser: A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset'
tags:
  - Python
  - MEDLINE
  - PubMed
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

Biomedical publications are increasing exponetially in the recent years. Due to the availability of such large-scale corpus from [PubMed](https://pubmed.ncbi.nlm.nih.gov/) and [MEDLINE](https://www.nlm.nih.gov/bsd/medline.html) database, researchers can mine the text and meta-data from such exploding of biomedical text. Examples of applications that can be built from biomedical text are ranged from predicting of novel drug-drug interaction, classifying biomedical text data, targeted search engine made for specified oncological profile, author name disambiguation, or automatic learning of biomedical ontology. Python has become one of the datascience tool that researchers use for building machine learning model or deep learning model to analyze text data. This is why we choose to build Pubmed Parser specifically for Python workflow.

Pubmed Parser is built as an Python data science tool for parsing open biomedical text data from MEDLINE dataset and Pubmed Open-Access data. It is built to parse incoming XML and HTML format to dictionary or JSON format easily used for the future data pre-processing. Moreover, the implemented functions can be scaled easily using parallel functionality using [PySpark](https://spark.apache.org/). This allow users to parse the most recently available corpus and customize for their need. Pubmed Parse has multiple functionailties, it can parse MEDLINE XML data, references from PubMed Open Access XML dataset, and many more.

Pubmed Parser has already been used in published work including [@achakulvisut2019claim; @vseva2019vist; @miller2017automated; @shahri2019propheno; @galea2018sub; @abdeddaim2018mesh; @rakhi2018data; @nikolov2018data; @mesbah2018smartpub; @neves2019evaluation; @tang2019parallel]. It is also been used in multiple biomedical and natural language class projects and blog posts due to the ease of implemented functionalities.


# Acknowledgements

Titipat Achakulvisut was supportyed by the Royal Thai Government Scholarship grant #50AC002. Daniel E. Acuna is supported by National Science Foundation #1800956.

# References