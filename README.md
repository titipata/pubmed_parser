# Parser for Pubmed Open-Access Subset XML Dataset and MEDLINE XML

[![Join the chat at https://gitter.im/titipata/pubmed_parser](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/titipata/pubmed_parser?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/titipata/pubmed_parser/blob/master/LICENSE)

Python parser for [PubMed open-access subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
(the download section of XML subset is at the end of the page, files are named like
  this `articles.A-B.tar.gz` ) and [MEDLINE XML](https://www.nlm.nih.gov/bsd/licensee/medpmmenu.html/)
  file.


## Parser available

#### Parse Pubmed OA XML information

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

```python
import pubmed_parser as pp
dict_out = pp.parse_pubmed_xml(path)
```

#### Parse Pubmed OA citations

We have `parse_pubmed_references` where you can give path to Pubmed Open Access XML
subset file and it will return list of dictionary that that particular PMID cites.
Each dictionary has keys as following

- `article_title`: article title
- `journal`: journal name
- `journal_type`: type of journal
- `pmid`: Pubmed ID
- `pmc`: Pubmed Central ID
- `pmid_cited`: Pubmed ID of cited article

```python
dicts_out = pp.parse_pubmed_references(path) # list of dictionary
```

#### Parse Pubmed OA captions

The function `parse_pubmed_caption` can parse image captions from given path
to XML file. It will return reference index that you can refer back to actual
images. The function will return list of dictionary which has following keys

- `pmc`:Pubmed ID
- `pmid`: Pubmed Central ID
- `fig_caption`: string of caption
- `fig_id`: reference id for figure (use to refer in XML article)
- `fig_label`: label of the figure
- `graphic_ref`: reference to graphic file name provided from Pubmed OA


#### Parse Medline XML

Medline has different format of XML file. You can use function `parse_medline_xml`
in order to parse XML file from full MEDLINE data. The license can be requested from this  [site](https://www.nlm.nih.gov/bsd/licensee/medpmmenu.html). The function will
return list of dictionary where each element contains:

- `title`: title of the article
- `abstract`: abstract of the article
- `affiliation`: first affiliation from the article
- `authors`: string of authors each separated by `;`
- `mesh_terms`: list of MESH terms related to the article each separated by `;`
- `year`: Publication year

```python
dicts_out = pp.parse_medline_xml(path) # list of dictionary
```


#### Parse Medline XML from eutils

You can use Pubmed parser to parse XML file from [eutils website](http://www.ncbi.nlm.nih.gov/books/NBK25501/)
using `parse_xml_web`. For this function, you can provide single `pmid` as an input.

```python
dict_out = pp.parse_xml_web(pmid, save_xml=False)
```


## Install package

Install all dependencies

```bash
$ pip install -r requirements.txt
```

Then you can install package using `setup.py` by running

```bash
$ python setup.py develop install
```


## Example Usage for Pubmed OA

Example code is shown below,

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


## Example Usage with PySpark

This script takes about 3.1 mins to parse all Pubmed Open-Access subset using PySpark on Amazon EC2 `r3.8xlarge` (with 32 cores).

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
- [unidecode](https://pypi.python.org/pypi/Unidecode)


## Citation

If you use this package, please cite it like this

<code>Titipat Achakulvisut, Daniel E. Acuna (2015) "Pubmed Parser" [http://github.com/titipata/pubmed_parser](http://github.com/titipata/pubmed_parser)</code>

## License

MIT License Copyright (c) 2015 Titipat Achakulvisut, Daniel E. Acuna
