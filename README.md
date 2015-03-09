#Parser for Pubmed Open-Access Subset XML Dataset

Python parser for [PubMed open-access subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/) (download section is at the end of the page)


##About

We create a simple parser for PubMed open-access subset where you can give
an XML path or string to the function called `parse_pubmed_xml` that will return
a dictionary with the following keys:

 - `full_title`: Article's title
 - `abstract`: Abstract
 - `journal_title`: Journal name or journal title
 - `pmid`: Pumed ID
 - `pmc`: Pumed Central ID
 - `publisher_id`: Publisher ID
 - `author_list`: list of authors and affiliation keys as `[['Last name 1', 'First Name 2', ['aff_key_1', 'aff_key_2', ...]],
['Last name 2', 'First Name 2', ['aff_key_1', ...]], ...]`
 - `affiliation_list`: Affiliation dictionary `{'aff_key_1' : 'Affiliation1', ...}`
 - `publication_year`: Publication year

##Example Usage:

```python
import pubmed_parser as pp
path_all_xml = pp.list_xmlpath('data') # list all xml path under directory
pubmed_dict = pp.parse_pubmed_xml(path_all_xml[0]) # dictionary output
print(pubmed_dict)

{'abstract': u"Background Despite identical genotypes and ...",
 'affiliation_list': {'I1': 'Department of Biological Sciences, ...',
  'I2': 'Biology Department, Queens College, and the Graduate Center ...'},
 'author_list': [['Dennehy', 'John J', ['I1', 'I2']],
  ['Wang', 'Ing-Nang', ['I1']]],
 'full_title': u'Factors influencing lysis time stochasticity in bacteriophage \u03bb',
 'journal_title': 'BMC Microbiology',
 'pmc': '3166277',
 'pmid': '21810267',
 'publication_year': '2011',
 'publisher_id': '1471-2180-11-174',
 'subjects': 'Research Article'}
```

You can also pass list of xml path to `create_pubmed_df` and it will return pandas DataFrame
including information from all the path in the given list (no more than 10k Pubmed path are recommended if you
don't do it in parallel). It takes about 0.4 days to parse all PubMed subset.

```python
import pubmed_parser as pp
path_all_xml = pp.list_xmlpath('data') # list all xml path under directory
pubmed_df = pp.create_pubmed_df(path_all_xml) # return DataFrame
```


##Members

- [Titipat Achakulvisut](http://titipata.github.io), Northwestern University
- [Daniel E. Acuna](http://scienceofscience.org/about), Rehabilitation Institute of Chicago and Northwestern University


##Dependencies

- [lxml](http://lxml.de/)
- [pandas](https://github.com/pydata/pandas)


##License

(c) 2015 Titipat Achakulvisut, Daniel E. Acuna
