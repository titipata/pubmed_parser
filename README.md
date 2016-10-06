# Parser for Pubmed Open-Access XML Subset and MEDLINE XML Dataset

[![Join the chat at https://gitter.im/titipata/pubmed_parser](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/titipata/pubmed_parser?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/titipata/pubmed_parser/blob/master/LICENSE)

Python parser for [PubMed Open-Access (OA) subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
 and [MEDLINE XML](https://www.nlm.nih.gov/bsd/licensee/) repository. See
 [wiki page](https://github.com/titipata/pubmed_parser/wiki) on how to download and
 process dataset using the repository.


## Parsers available

**note** path can be path to compressed or uncompressed xml file. We provide example
file in [`data`](data/) folder

#### Parse Pubmed OA XML information

We created a simple parser for PubMed Open Access Subset where you can give
an XML path or string to the function called `parse_pubmed_xml` which will return
a dictionary with the following information:

 - `full_title`: article's title
 - `abstract`: abstract
 - `journal`: Journal name
 - `pmid`: Pubmed ID
 - `pmc`: Pubmed Central ID
 - `doi`: DOI of the article
 - `publisher_id`: publisher ID
 - `author_list`: list of authors with affiliation keys in the following format

 ```python
 [['last_name_1', 'first_name_1', 'aff_key_1'],
  ['last_name_1', 'first_name_1', 'aff_key_2'],
  ['last_name_2', 'first_name_2', 'aff_key_1'], ...]
 ```
 - `affiliation_list`: list of affiliation keys and affiliation strings in the following format
 ```python
 [['aff_key_1', 'affiliation_1'],
  ['aff_key_2', 'affiliation_2'], ...]
 ```

 - `publication_year`: publication year
 - `subjects`: list of subjects listed in the article separated by semicolon.
 Sometimes, it only contains type of article, such as research article, review, proceedings, etc.

```python
import pubmed_parser as pp
dict_out = pp.parse_pubmed_xml(path)
```

#### Parse Pubmed OA citation references

The function `parse_pubmed_references` will process a Pubmed Open Access XML
file and return a list of the PMID it cites.
Each dictionary has keys as follows

- `article_title`: title of cited article
- `journal`: journal name
- `journal_type`: type of journal
- `pmid`: Pubmed ID of the article
- `pmc`: Pubmed Central ID of the article
- `pmid_cited`: Pubmed ID of article that given article cites

```python
dicts_out = pp.parse_pubmed_references(path) # return list of dictionary
```

#### Parse Pubmed OA images and captions

The function `parse_pubmed_caption` can parse image captions from given path
to XML file. It will return reference index that you can refer back to actual
images. The function will return list of dictionary which has following keys

- `pmid`: Pubmed ID
- `pmc`: Pubmed Central ID
- `fig_caption`: string of caption
- `fig_id`: reference id for figure (use to refer in XML article)
- `fig_label`: label of the figure
- `graphic_ref`: reference to image file name provided from Pubmed OA

```python
dicts_out = pp.parse_pubmed_caption(path) # return list of dictionary
```

#### Parse Pubmed OA Paragraph

For someone who might be interested in parsing the text surrounding
a citation, the library also provides that functionality.
You can use `parse_pubmed_paragraph` to parse text and reference PMIDs.
This function will return a list of dictionaries, where each entry will have
following keys

- `pmid`: Pubmed ID
- `pmc`: Pubmed Central ID
- `text`: full text of the paragraph
- `references_pmids`: list of reference PMIDs
- `references_code`: list of reference code within that paragraph
- `section`: section of paragraph (e.g. Background, Discussion, Appendix)

#### Parse Pubmed OA Table [WIP]

You can use `parse_pubmed_table` to parse table from XML file. This function
will return list of dictionaries where each has following keys.

- `pmid`: Pubmed ID
- `pmc`: Pubmed Central ID
- `caption`: caption of the table
- `label`: lable of the table
- `table_columns`: list of column name
- `table_values`: list of values inside the table
- `table_xml`: raw xml text of the table (return if `return_xml=True`)

```python
dicts_out = pp.parse_pubmed_table('data/medline16n0902.xml.gz', return_xml=False)
```

#### Parse Medline NML XML

Medline NML XML has a different XML format than PubMed Open Access.
You can use the function `parse_medline_xml` to parse that format.
This function will return list of dictionaries, where each element contains:

- `pmid`: Pubmed ID
- `pmc`: Pubmed Central ID
- `title`: title of the article
- `abstract`: abstract of the article
- `affiliation`: corresponding author's affiliation
- `authors`: authors, each separated by `;`
- `mesh_terms`: list of MeSH terms, each separated by `;`
- `keywords`: list of keywords, each separated by `;`
- `pubdate`: Publication date. Defaults to year information only.

```python
dicts_out = pp.parse_medline_xml('data/medline16n0902.xml.gz') # return list of dictionary
```

Try to extract month and day information from PubDate as well:

```python
dicts_out = pp.parse_medline_xml('data/medline16n0902.xml.gz', year_info_only=False)  
```

#### Parse Medline Grant ID

Use `parse_medline_grant_id` in order to parse MEDLINE grant IDs from XML file.
This will return a list of dictionaries, each containing

- `pmid`: Pubmed ID
- `grant_id`: Grant ID
- `grant_acronym`: Acronym of grant
- `country`: Country where grant funding from
- `agency`: Grant agency

If no Grant ID is found, it will return `None`


#### Parse Medline XML from eutils website

You can use PubMed parser to parse XML file from [E-Utilities](http://www.ncbi.nlm.nih.gov/books/NBK25501/)
using `parse_xml_web`. For this function, you can provide a single `pmid` as an input and
get a dictionary with following keys

- `title`: title
- `abstract`: abstract
- `journal`: journal
- `affiliation`: affiliation of first author
- `authors`: string of authors, separated by `;`
- `year`: Publication year

```python
dict_out = pp.parse_xml_web(pmid, save_xml=False)
```

#### Parse Medline XML citations from website

The function `parse_citation_web` allows you to get the citations to a given
PubMed ID or PubMed Central ID. This will return a dictionary which contains the following keys

- `pmc`: Pubmed Central ID
- `pmid`: Pubmed ID
- `doi`: DOI of the article
- `n_citations`: number of citations for given articles
- `pmc_cited`: list of PMCs that cite the given PMC

```python
dict_out = pp.parse_citation_web(doc_id, id_type='PMC')
```

#### Parse Outgoing XML citations from website

The function `parse_outgoing_citation_web` allows you to get the articles a given
article cites, given a PubMed ID or PubMed Central ID. This will return a dictionary
which contains the following keys

- `n_citations`: number of cited articles
- `doc_id`: the document identifier given
- `id_type`: the type of identifier given. Either 'PMID' or 'PMC'
- `pmid_cited`: list of PMIDs cited by the article

```python
dict_out = pp.parse_outgoing_citation_web(doc_id, id_type='PMID')
```

Identifiers should be passed as strings. PubMed Central ID's are default, and
should be passed as strings *without* the 'PMC' prefix. If no citations are
found, or if no article is found matching `doc_id` in the indicated database,
it will return `None`.


## Install package

Install all dependencies

```bash
$ pip install -r requirements.txt
```

Then you can install the package as follows

```bash
$ python setup.py install
```


## Example Usage for Pubmed OA

An example usage is shown as follows

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
 'journal': 'BMC Microbiology',
 'pmc': '3166277',
 'pmid': '21810267',
 'publication_year': '2011',
 'publisher_id': '1471-2180-11-174',
 'subjects': 'Research Article'}
```


## Example Usage with PySpark

This script takes about 3.1 mins to parse all Pubmed Open Access subset using
PySpark on Amazon EC2 `r3.8xlarge`.

```python
import pandas as pd
import pubmed_parser as pp
path_all = pp.list_xml_path('/path/to/folder/')
path_rdd = sc.parallelize(path_all, numSlices=10000)
pubmed_oa_all = path_rdd.map(lambda p: pp.parse_pubmed_xml(p)).collect() # load to memory
# path_rdd.map(lambda p: pp.parse_pubmed_xml(p)).saveAsPickleFile('pubmed_oa.pickle') # or to save to pickle
pubmed_oa_df = pd.DataFrame(pubmed_oa_all) # transform to pandas DataFrame
```

See [scripts](https://github.com/titipata/pubmed_parser/tree/master/scripts)
folder for more information.


## Members

- [Titipat Achakulvisut](http://titipata.github.io), Northwestern University
- [Daniel E. Acuna](http://scienceofscience.org/about), Rehabilitation Institute of Chicago and Northwestern University

and [contributors](https://github.com/titipata/pubmed_parser/graphs/contributors)


## Dependencies

- [lxml](http://lxml.de/)
- [unidecode](https://pypi.python.org/pypi/Unidecode)
- [requests](http://docs.python-requests.org/en/master/)

## Citation

If you use this package, please cite it like this

> Titipat Achakulvisut, Daniel E. Acuna (2015) "_Pubmed Parser_" [http://github.com/titipata/pubmed_parser](http://github.com/titipata/pubmed_parser)


## Acknowledgement

Package is developed in [Konrad Kording's Lab](http://kordinglab.com/) at Northwestern University


## License

MIT License Copyright (c) 2015, 2016 Titipat Achakulvisut, Daniel E. Acuna
