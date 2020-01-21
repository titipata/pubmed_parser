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

The number of biomedical publications is increasing exponentially every year. If we had the ability to access, manipulate, and link this information, we could extract knowledge that is perhaps hidden within the figures, text, and citations. In particular, the repositories made available by the [PubMed](https://pubmed.ncbi.nlm.nih.gov/) and [MEDLINE](https://www.nlm.nih.gov/bsd/medline.html) databases enable these kinds of applications at an unprecedented level. Examples of applications that can be built from this dataset range from predicting novel drug-drug interactions, classifying biomedical text data, searching specific oncological profiles, disambiguating author names, or automatically learning a biomedical ontology. Here, we propose Pubmed Parser (`pubmed_parser`), a software to mine Pubmed and MEDLINE efficiently. Pubmed Parser is built on top of Python and can therefore be integrated into a myriad of tools for machine learning such as `scikit-learn` and deep learning such as `tensorflow` and `pytorch`.

Pubmed Parser has the capability of parsing multiple refined information into structured datasets that former developed libraries such as [`medic`](https://github.com/fnl/medic) or [`MEDLINEXMLToJSON`](https://github.com/ldbib/MEDLINEXMLToJSON) do not have. `medic`, for example, does not output paragraphs and captions and has been discountinued since 2015. `MEDLINEXMLToJSON`, similary, transforms the original XML files into a JSON file, keeping the same structure. It seems also that `MEDLINEXMLToJSON` has been discountinued since 2016. Our parser can be used within Python and provides results in dictionaries
```python
import pubmed_parser as pp
pp.parse_pubmed_xml(path_to_xml)
```
```python
{'abstract': u"Background Despite identical genotypes and ...",
 'affiliation_list':
  [['I1': 'Department of Biological Sciences, ...'],
   ['I2': 'Biology Department, Queens College, and the Graduate Center ...']],
  'author_list':
  [['Dennehy', 'John J', 'I1'],
   ['Dennehy', 'John J', 'I2'],
   ['Wang', 'Ing-Nang', 'I1']],
 'full_title': u'Factors influencing lysis time stochasticity in bacteriophage \u03bb',
 'journal': 'BMC Microbiology',
 'pmc': '3166277',
 'pmid': '21810267',
 'publication_year': '2011',
 'publisher_id': '1471-2180-11-174',
 'subjects': 'Research Article'}
```
It can parse multiple PubMed and MEDLINE data derivatives including articles' information, authors and affiliations, references, figure captions, paragraphs, and more. For example, Pubmed Parser can be integrated to researchers' workflow to parse list of authorship and their associated metadata such as affiliation and MeSH terms for a large-scale name disambiguation pipeline [@tang2019parallel]. It has also be used in deep learning pipeline such as scientific articles summarization by using pair of title and abstract parsed from MEDLINE and PubMed articles [@nikolov2018data]. Parsing XML and HTML with Pubmed Parser is extremely fast: this is a core feature of the package that allows producing either dictionaries or JSON files that can easily be part of downstream pipelines. Moreover, the implemented functions can be scaled easily as part of other MapReduce-like infrastructure such as [PySpark](https://spark.apache.org/). This allows users to parse the most recently available corpus and customize the parsing to their needs. Below, we provide an example code to parse an XML file from [MEDLINE corpus](https://www.nlm.nih.gov/databases/download/data_distrib_main.html).

``` python
import pubmed_parser as pp
parsed_articles = pp.parse_medline_xml('data/medline16n0902.xml.gz',
                                       year_info_only=True,
                                       nlm_category=False,
                                       author_list=False)
```

Pubmed Parser has already been used in published work for several different purposes, including authors name disambiguation [@tang2019parallel], information extraction and summarization [@mesbah2018smartpub; @nikolov2018data; @achakulvisut2019claim; @abdeddaim2018mesh; @galea2018sub], search engine optimization [@shahri2019propheno; @vseva2019vist], and novel biomedical discovery [@miller2017automated; @shahri2019propheno; @rakhi2018data]. It has also been used in multiple biomedical and natural language class projects, and various data science blog posts relating to biomedical text analysis.

# Acknowledgements

Titipat Achakulvisut was supportyed by the Royal Thai Government Scholarship grant #50AC002. Daniel E. Acuna is supported by National Science Foundation #1800956.

# References
