#Parser for Pubmed Open-Access Subset XML Dataset

Python parser for PubMed open-access subset.


##Usage

We create a simple parser for PubMed open-access dataset where you can give 
an XML path or string to the function called `pare_pubmed_xml` that will return
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

Example Usage:

```python
import pubmed_parser as pp
path_all_xml = pp.list_xmlpath('/<path_to>/pubmed_data/') # list all xml path under directory
pubmed_list = pp.parse_pubmed_xml(path_all_xml[0]) # dictionary output
```

You can also pass list of xml path to `create_pubmed_df` and it will return pandas DataFrame
including information from all the path in the given list (no more than 10k Pubmed path are recommended if you 
don't do it in parallel)

```python
import pubmed_parser as pp
n = 10000
path_all_xml = pp.list_xmlpath('/<path_to>/pubmed_data/')
pubmed_df = pp.create_pubmed_df(path_all_xml[0:n]) # return DataFrame
```


##Members

- [Titipat Achakulvisut](http://titipata.github.io), Northwestern University
- [Daniel E. Acuna](http://scienceofscience.org/about), Rehabilitation Institute of Chicago and Northwestern University


##Dependencies

- [lxml](http://lxml.de/)
- [pandas](https://github.com/pydata/pandas)


##License

(c) 2015 Titipat Achakulvisut, Daniel E. Acuna
