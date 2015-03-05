#Parser for Pubmed Open-Source XML data

Python simple parser for PubMed open source data. 
People use 

##Members

- [Titipat Achakulvisut](http://titipata.github.io)
- [Daniel E. Acuna](http://scienceofscience.org/about), Rehabilitation Institute of Chicago and Northwestern University

##Usage

We create a simple parser where you can give xml path 
to function called `extract_pubmed_xml` and it will return 
list of `[article_name, topic, abstract, journal_title, pubmed_id, pmc, pub_id, all_aff, aff_dict, pub_year]`, 
for example:

```python
path_all_xml = list_xmlpath('/<path_to>/pubmed_data/') # this will list all xml path under directory
pubmed_list = extract_pubmed_xml(path_all_xml[0])
```

You can also pass list of xml path to `create_pubmed_df` and it will return pandas DataFrame 
including information from all the path in the given list

```python
from pubmed_parser import *
n = 10000
path_all_xml = list_xmlpath('/<path_to>/pubmed_data/') # this will list all xml path under directory
pubmed_df = create_pubmed_df(path_all_xml[0:n])
```

##Dependencies

- [NumPy](https://github.com/numpy/numpy)
- [lxml](http://lxml.de/)
- [pandas](https://github.com/pydata/pandas)

##License

(c) 2015 Titipat Achakulvisut, Daniel E. Acuna
