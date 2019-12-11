---
title: 'Pubmed Parser: A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset
  XML Dataset'
authors:
- affiliation: 1
  name: Titipat Achakulvisut
- affiliation: 2
  name: Daniel E. Acuna
- affiliation: 3
  name: Ted Cybulski
- affiliation: 1
  name: Konrad Kording
date: "15 December 2019"
output: pdf_document
bibliography: paper.bib
tags:
- Python
- MEDLINE
- PubMed
- Biomedical corpus
- Natural Language Processing
affiliations:
- index: 1
  name: University of Pennsylvania
- index: 2
  name: Syracuse University
- index: 3
  name: Northwestern University
---

# Summary

Biomedical publications are increasing exponentially every year. If we had the ability to access, manipulate, and link this information, we could extract knowledge that is perhaps hidden within the figures, text, and citations. In particular, the repositories made avilable by [PubMed](https://pubmed.ncbi.nlm.nih.gov/) and [MEDLINE](https://www.nlm.nih.gov/bsd/medline.html) database enable these kinds of applications at an unprecedented level. Examples of applications that can be built from this dataset range from predicting novel drug-drug interactions, classifying biomedical text data, searching specific oncological profiles, disambiguating author names, or automatically learning a biomedical ontology. Here, we propose Pubmed Parser (`pubmed_parser`), a software to mine Pubmed and MEDLINE efficiently. Pubmed Parser is built on top of Python and can therefore be integrated into a myriad of tools for machine learning such as `scikit-learn` and deep learning such as `tensorflow` and `pytorch`.

Pubmed Parser has a capability to parse multiple refined information into structured dataset that former developed libraries such as [`medic`](https://github.com/fnl/medic) or [`MEDLINEXMLToJSON`](https://github.com/ldbib/MEDLINEXMLToJSON) do not have. It can parse multiple Pubmed MEDLINE data derivatives such as MEDLINE XML data, references from PubMed Open Access XML dataset, figure captions, paragraphs, and more. A core part of the package, parsing XML and HTML with Pubmed Parser is extremely fast, producing either dictionaries or JSON files that can easily be part of downstream pipelines. Moreover, the implemented functions can be scaled easily as part of other MapReduce-like infrastructure such as [PySpark](https://spark.apache.org/). This allows users to parse the most recently available corpus and customize the parsing to their needs.

Pubmed Parser has already been used in published work including authors name disambiguation [@tang2019parallel], information extraction and summarization [@mesbah2018smartpub; @nikolov2018data; @achakulvisut2019claim; @abdeddaim2018mesh; @galea2018sub], search engine optimization [@shahri2019propheno; @vseva2019vist], and novel biomedical discovery [@miller2017automated; @shahri2019propheno; @rakhi2018data]. It has also been used in multiple biomedical and natural language class projects, and various data science blog posts relating to biomedical text analysis.

# Acknowledgements

Titipat Achakulvisut was supportyed by the Royal Thai Government Scholarship grant #50AC002. Daniel E. Acuna is supported by National Science Foundation #1800956.

# References