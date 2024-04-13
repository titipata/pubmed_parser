# Pubmed Parser: A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/titipata/pubmed_parser/blob/master/LICENSE) [![DOI](https://joss.theoj.org/papers/10.21105/joss.01979/status.svg)](https://doi.org/10.21105/joss.01979)
 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3660006.svg)](https://doi.org/10.5281/zenodo.3660006) [![Build Status](https://travis-ci.com/titipata/pubmed_parser.svg?branch=master)](https://travis-ci.com/titipata/pubmed_parser)

Pubmed Parser is a Python library for parsing the [PubMed Open-Access (OA) subset](http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/)
 , [MEDLINE XML](https://www.nlm.nih.gov/bsd/licensee/) repositories, and [Entrez Programming Utilities (E-utils)](https://eutils.ncbi.nlm.nih.gov/). It uses the `lxml` library to parse this information into a Python dictionary which can be easily used for research, such as in text mining and natural language processing pipelines.

For available APIs and details about the dataset, please see our [wiki page](https://github.com/titipata/pubmed_parser/wiki) or
 [documentation page](http://titipata.github.io/pubmed_parser/) for more details. Below, we list some of the core funtionalities and code examples.

## Available Parsers

* `path` provided to a function can be the path to a compressed or uncompressed XML file. We provide example files in the [ `data` ](data/) folder.
* for website parsing, you should scrape with pause. Please see the [copyright notice](https://www.ncbi.nlm.nih.gov/pmc/about/copyright/#copy-PMC) because your IP can get blocked if you try to download in bulk.

Below, we list available parsers from `pubmed_parser`.

  * [Parse PubMed OA XML information](#parse-pubmed-oa-xml-information)
  * [Parse PubMed OA citation references](#parse-pubmed-oa-citation-references)
  * [Parse PubMed OA images and captions](#parse-pubmed-oa-images-and-captions)
  * [Parse PubMed OA Paragraph](#parse-pubmed-oa-paragraph)
  * [Parse PubMed OA Table [WIP]](#parse-pubmed-oa-table-wip)
  * [Parse MEDLINE XML](#parse-medline-xml)
  * [Parse MEDLINE Grant ID](#parse-medline-grant-id)
  * [Parse MEDLINE XML from eutils website](#parse-medline-xml-from-eutils-website)
  * [Parse MEDLINE XML citations from website](#parse-medline-xml-citations-from-website)
  * [Parse Outgoing XML citations from website](#parse-outgoing-xml-citations-from-website)

### Parse PubMed OA XML information

We created a simple parser for the PubMed Open Access Subset where you can give an XML path or string to the function called `parse_pubmed_xml` which will return a dictionary with the following information:

* `full_title` : article's title
* `abstract` : abstract
* `journal` : Journal name
* `pmid` : PubMed ID
* `pmc` : PubMed Central ID
* `doi` : DOI of the article
* `publisher_id` : publisher ID
* `author_list` : list of authors with affiliation keys in the following format

``` python
 [['last_name_1', 'first_name_1', 'aff_key_1'],
  ['last_name_1', 'first_name_1', 'aff_key_2'],
  ['last_name_2', 'first_name_2', 'aff_key_1'], ...]
 ```

* `affiliation_list` : list of affiliation keys and affiliation strings in the following format

``` python
 [['aff_key_1', 'affiliation_1'],
  ['aff_key_2', 'affiliation_2'], ...]
```

* `publication_year` : publication year
* `subjects` : list of subjects listed in the article separated by semicolon. Sometimes, it only contains the type of the article, such as a research article, review proceedings, etc.

``` python
import pubmed_parser as pp
dict_out = pp.parse_pubmed_xml(path)
```

### Parse PubMed OA citation references

The function `parse_pubmed_references` will process a Pubmed Open Access XML file and return a list of the PMIDs it cites. Each dictionary has keys as follows

* `pmid` : PubMed ID of the article
* `pmc` : PubMed Central ID of the article
* `article_title` : title of cited article
* `journal` : journal name
* `journal_type` : type of journal
* `pmid_cited` : PubMed ID of article that article cites
* `doi_cited` : DOI of article that article cites
* `year` : Publication year as it appears in the reference (may include letter suffix, e.g.2007a)

``` python
dicts_out = pp.parse_pubmed_references(path) # return list of dictionary
```

### Parse PubMed OA images and captions

The function `parse_pubmed_caption` can parse image captions from a given path to XML file. It will return reference index that you can refer back to actual images. The function will return list of dictionary which has following keys

* `pmid` : PubMed ID
* `pmc` : PubMed Central ID
* `fig_caption` : string of caption
* `fig_id` : reference id for figure (use to refer in XML article)
* `fig_label` : label of the figure
* `graphic_ref` : reference to image file name provided from Pubmed OA

``` python
dicts_out = pp.parse_pubmed_caption(path) # return list of dictionary
```

### Parse PubMed OA Paragraph

For someone who might be interested in parsing the text surrounding a citation, the library also provides that functionality. You can use `parse_pubmed_paragraph` to parse text and reference PMIDs. This function will return a list of dictionaries, where each entry will have following keys:

* `pmid` : PubMed ID
* `pmc` : PubMed Central ID
* `text` : full text of the paragraph
* `reference_ids` : list of reference code within that paragraph.

This IDs can merge with output from `parse_pubmed_references` .

* `section` : section of paragraph (e.g. Background, Discussion, Appendix, etc.)

``` python
dicts_out = pp.parse_pubmed_paragraph('data/6605965a.nxml', all_paragraph=False)
```

### Parse PubMed OA Table [WIP]

You can use `parse_pubmed_table` to parse table from XML file. This function will return list of dictionaries where each has following keys.

* `pmid` : PubMed ID
* `pmc` : PubMed Central ID
* `caption` : caption of the table
* `label` : lable of the table
* `table_columns` : list of column name
* `table_values` : list of values inside the table
* `table_xml` : raw xml text of the table (return if `return_xml=True`)

``` python
dicts_out = pp.parse_pubmed_table('data/medline16n0902.xml.gz', return_xml=False)
```

### Parse MEDLINE XML

MEDLINE XML has a different XML format than PubMed Open Access. The structure of XML files can be found in MEDLINE/PubMed DTD [here](https://www.nlm.nih.gov/databases/dtd/). You can use the function `parse_medline_xml` to parse that format. This function will return list of dictionaries, where each element contains:

* `pmid` : PubMed ID
* `pmc` : PubMed Central ID
* `doi` : DOI
* `other_id` : Other IDs found, each separated by `;`
* `title` : title of the article
* `abstract` : abstract of the article
* `authors` : authors, each separated by `;`
* `mesh_terms` : list of MeSH terms with corresponding MeSH ID, each separated by `;` e.g. `'D000161:Acoustic Stimulation; D000328:Adult; ...`
* `publication_types` : list of publication type list each separated by `;` e.g. `'D016428:Journal Article'`
* `keywords` : list of keywords, each separated by `;`
* `chemical_list` : list of chemical terms, each separated by `;`
* `pubdate` : Publication date. Defaults to year information only.
* `journal` : journal of the given paper
* `medline_ta` : this is abbreviation of the journal name
* `nlm_unique_id` : NLM unique identification
* `issn_linking` : ISSN linkage, typically use to link with Web of Science dataset
* `country` : Country extracted from journal information field
* `reference` : string of PMID each separated by `;` or list of references made to the article
* `delete` : boolean if `False` means paper got updated so you might have two
* `languages` : list of languages, separated by `;`
* `vernacular_title`: vernacular title. Defaults to empty string whenever non-available.

XMLs for the same paper. You can delete the record of deleted paper because it got updated.

``` python
dicts_out = pp.parse_medline_xml('data/medline16n0902.xml.gz',
                                 year_info_only=False,
                                 nlm_category=False,
                                 author_list=False,
                                 reference_list=False) # return list of dictionary
```

To extract month and day information from PubDate, set `year_info_only=True`. We also allow parsing structured abstract and we can control display of each section or label by changing `nlm_category` argument.

### Parse MEDLINE Grant ID

Use `parse_grant_id` in order to parse MEDLINE grant IDs from XML file. This will return a list of dictionaries, each containing

* `pmid` : PubMed ID
* `grant_id` : Grant ID
* `grant_acronym` : Acronym of grant
* `country` : Country where grant funding from
* `agency` : Grant agency

If no Grant ID is found, it will return `None`

### Parse MEDLINE XML from eutils website

You can use PubMed parser to parse XML file from [E-Utilities](http://www.ncbi.nlm.nih.gov/books/NBK25501/) using `parse_xml_web` . For this function, you can provide a single `pmid` as an input and get a dictionary with following keys

* `title` : title
* `abstract` : abstract
* `journal` : journal
* `affiliation` : affiliation of first author
* `authors` : string of authors, separated by `;`
* `year` : Publication year
* `keywords` : keywords or MESH terms of the article

``` python
dict_out = pp.parse_xml_web(pmid, save_xml=False)
```

### Parse MEDLINE XML citations from website

The function `parse_citation_web` allows you to get the citations to a given PubMed ID or PubMed Central ID. This will return a dictionary which contains the following keys

* `pmc` : PubMed Central ID
* `pmid` : PubMed ID
* `doi` : DOI of the article
* `n_citations` : number of citations for given articles
* `pmc_cited` : list of PMCs that cite the given PMC

``` python
dict_out = pp.parse_citation_web(doc_id, id_type='PMC')
```

### Parse Outgoing XML citations from website

The function `parse_outgoing_citation_web` allows you to get the articles a given article cites, given a PubMed ID or PubMed Central ID. This will return a dictionary which contains the following keys

* `n_citations` : number of cited articles
* `doc_id` : the document identifier given
* `id_type` : the type of identifier given. Either `'PMID'` or `'PMC'`
* `pmid_cited` : list of PMIDs cited by the article

``` python
dict_out = pp.parse_outgoing_citation_web(doc_id, id_type='PMID')
```

Identifiers should be passed as strings. PubMed Central ID's are default, and should be passed as strings *without* the `'PMC'` prefix. If no citations are found, or if no article is found matching `doc_id` in the indicated database, it will return `None`.

## Installation

You can install the most update version of the package directly from the repository

``` bash
pip install git+https://github.com/titipata/pubmed_parser.git
```

or install recent release with [PyPI](https://pypi.org/project/pubmed-parser/) using

``` bash
pip install pubmed-parser
```

or clone the repository and install using `pip`

``` bash
git clone https://github.com/titipata/pubmed_parser
pip install ./pubmed_parser
```

You can test your installation by running `pytest --cov=pubmed_parser tests/ --verbose`
in the root of the repository.

## Example snippet to parse PubMed OA dataset

An example usage is shown as follows

``` python
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

This is a snippet to parse all PubMed Open Access subset using [PySpark 2.1](https://spark.apache.org/docs/latest/api/python/index.html)

``` python
import os
import pubmed_parser as pp
from pyspark.sql import Row

path_all = pp.list_xml_path('/path/to/xml/folder/')
path_rdd = spark.sparkContext.parallelize(path_all, numSlices=10000)
parse_results_rdd = path_rdd.map(lambda x: Row(file_name=os.path.basename(x),
                                               **pp.parse_pubmed_xml(x)))
pubmed_oa_df = parse_results_rdd.toDF() # Spark dataframe
pubmed_oa_df_sel = pubmed_oa_df[['full_title', 'abstract', 'doi',
                                 'file_name', 'pmc', 'pmid',
                                 'publication_year', 'publisher_id',
                                 'journal', 'subjects']] # select columns
pubmed_oa_df_sel.write.parquet('pubmed_oa.parquet', mode='overwrite') # write dataframe
```

See [scripts](https://github.com/titipata/pubmed_parser/tree/master/scripts)
folder for more information.

## Core Members

* [Titipat Achakulvisut](http://titipata.github.io)
* [Daniel E. Acuna](http://scienceofscience.org/about)

and [contributors](https://github.com/titipata/pubmed_parser/graphs/contributors)

## Dependencies

* [lxml](http://lxml.de/)
* [unidecode](https://pypi.python.org/pypi/Unidecode)
* [requests](http://docs.python-requests.org/en/master/)

## Citation

If you use Pubmed Parser, please cite it from [JOSS](https://joss.theoj.org/papers/10.21105/joss.01979) as follows

> Achakulvisut et al., (2020). Pubmed Parser: A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset XML Dataset. Journal of Open Source Software, 5(46), 1979, https://doi.org/10.21105/joss.01979

or using BibTex

```
@article{Achakulvisut2020,
  doi = {10.21105/joss.01979},
  url = {https://doi.org/10.21105/joss.01979},
  year = {2020},
  publisher = {The Open Journal},
  volume = {5},
  number = {46},
  pages = {1979},
  author = {Titipat Achakulvisut and Daniel Acuna and Konrad Kording},
  title = {Pubmed Parser: A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset XML Dataset},
  journal = {Journal of Open Source Software}
}
```

## Contributions

We welcome contributions from anyone who would like to improve Pubmed Parser. You can create [GitHub issues](https://github.com/titipata/pubmed_parser/issues) to discuss questions or issues relating to the repository. We suggest you to read our [Contributing Guidelines](https://github.com/titipata/pubmed_parser/blob/master/CONTRIBUTING.md) before creating issues, reporting bugs, or making a contribution to the repository.

## Acknowledgement

This package is developed in [Konrad Kording's Lab](http://kordinglab.com/) at the University of Pennsylvania. We would like to thank reviewers and the editor from [JOSS](https://joss.readthedocs.io/en/latest/) including [`tleonardi`](https://github.com/tleonardi), [`timClicks`](https://github.com/timClicks), and [`majensen`](https://github.com/majensen). They made our repository much better!

## License

MIT License Copyright (c) 2015-2020 Titipat Achakulvisut, Daniel E. Acuna
