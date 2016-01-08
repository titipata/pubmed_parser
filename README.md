# Parser for Pubmed Open-Access Subset XML Dataset

[![Join the chat at https://gitter.im/titipata/pubmed_parser](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/titipata/pubmed_parser?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Python parser for [PubMed open-access subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/) (the download section of XML subset is at the end of the page, files are named like this `articles.A-B.tar.gz` )


## About

We created a simple parser for PubMed Open Access Subset where you can give
an XML path or string to the function called `parse_pubmed_xml` which will return
a dictionary with the following information:

 - `full_title`: article's title
 - `abstract`: abstract
 - `journal_title`: Journal name or journal title
 - `pmid`: Pubmed ID
 - `pmc`: Pubmed Central ID
 - `publisher_id`: publisher ID
 - `author_list`: list of authors with affiliation keys in following format

 ```python
 [['last_name_1', 'first_name_1', 'aff_key_1'],
  ['last_name_1', 'first_name_1', 'aff_key_2'],
  ['last_name_2', 'first_name_2', 'aff_key_1'], ...]
 ```
 - `affiliation_list`: list of affiliation keys and affiliation string in following format
 ```python
 [['aff_key_1' : 'affiliation_1'],
  ['aff_key_2' : 'affiliation_2'], ...]
 ```

 - `publication_year`: publication year
 - `subjects`: list of subjects listed in the article. Sometimes, it only contains what type of article it is, such as research article, review, proceedings, etc.


## Example Usage

```python
import pubmed_parser as pp
path_xml = pp.list_xml_path('data') # list all xml paths under directory
pubmed_dict = pp.parse_pubmed_xml(path_xml[0]) # dictionary output
print(pubmed_dict)

{'abstract': u"Background Despite identical genotypes and ...",
 'affiliation_list':
  [['I1': 'Department of Biological Sciences, ...'],
   ['I2': 'Biology Department, Queens College, and the Graduate Center ...']],
  'author_list':
  [['Dennehy', 'John J', 'I1'],
   ['Dennehy', 'John J', 'I2'],
   ['Wang', 'Ing-Nang', 'I1']],
 'full_title': u'Factors influencing lysis time stochasticity in bacteriophage \u03bb',
 'journal_title': 'BMC Microbiology',
 'pmc': '3166277',
 'pmid': '21810267',
 'publication_year': '2011',
 'publisher_id': '1471-2180-11-174',
 'subjects': 'Research Article'}
```

You can also pass a list of XML paths to the function `parse_pubmed_xml_to_df` which will return the parsed information in DataFrame format of all the XMLs in the given list. Providing less than 10k XML paths are recommended if you do not parse in parallel since it can crash the memory. It takes about 0.4 days to parse all PubMed Open Access subset, which has around a million files.

```python
import pubmed_parser as pp
path_xml = pp.list_xml_path('data') # list all xml paths under given directory
pubmed_df = pp.parse_pubmed_xml_to_df(path_xml, include_path=True) # return DataFrame
```


## Example Usage for PySpark

This script takes about 3.1 mins on EC2 `r3.8xlarge` (with 32 cores) using PySpark on full Pubmed OA subset.

```python
import pandas as pd
import pubmed_parser as pp
path_all = pp.list_xml_path('/path/to/folder/')
path_rdd = sc.parallelize(path_all, numSlices=10000)
pubmed_oa_all = path_rdd.map(lambda p: pp.parse_pubmed_xml(p)).collect() # load to memory
# path_rdd.map(lambda p: pp.parse_pubmed_xml(p)).saveAsPickleFile('/mnt/daniel/pubmed_oa.pickle') # or to save to pickle
pubmed_oa_df = pd.DataFrame(pubmed_oa_all) # transform to pandas DataFrame
```


## Members

- [Titipat Achakulvisut](http://titipata.github.io), Northwestern University
- [Daniel E. Acuna](http://scienceofscience.org/about), Rehabilitation Institute of Chicago and Northwestern University


## Dependencies

- [lxml](http://lxml.de/)
- [pandas](https://github.com/pydata/pandas)


## Citation

If you use this package, please cite it like this

<code>Titipat Achakulvisut, Daniel E. Acuna (2015) "Pubmed Parser" [http://github.com/titipata/pubmed_parser](http://github.com/titipata/pubmed_parser)</code>

## License

(c) 2015 Titipat Achakulvisut, Daniel E. Acuna
