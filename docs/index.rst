.. Pubmed Parser documentation master file, created by
   sphinx-quickstart on Tue Jan 21 20:26:52 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pubmed Parser: A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset
========================================================================================


Pubmed Parser is a Python library for parsing the `PubMed Open-Access (OA) subset <http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/>`_
and `MEDLINE XML <https://www.nlm.nih.gov/bsd/licensee/>`_ repositories. 
It uses `lxml` library to parse this information into a Python dictionary which can be easily used for research such in text mining and natural language processing pipelines. 
See our `Wiki page <https://github.com/titipata/pubmed_parser/wiki/>`_ or this documentation on how to download and process dataset using the repository.


About the dataset
=================

`PubMed Open-Access (OA) subset <http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/>`_ contains XMLs of a full submitted papers which has 
information that you might get from a regular PDF article file but in a more structured format. `MEDLINE XML <https://www.nlm.nih.gov/bsd/licensee/>`_ 
contains about 30M biomedical articles published until now. We can access information until abstracts from a compressed XML file.
Other information such as number of citations of an article can be query through `Entrez Programming Utilities (E-utils) <https://eutils.ncbi.nlm.nih.gov/>`_
which can be obtained in XML format.

To work with the data, normally, you have to write an XML to parse these XMLs which can take time and effort. Pubmed Parser aims to reduce
those development by giving a high level functionalities so that researchers can obtain the dataset to analyze fast. It is also developed by researchers
who use these data so that we always keep it up-to-date.


Contents
========

.. toctree::
   :maxdepth: 1

   install
   api
   resources
   spark


Questions / Contributions / Bugs
================================

We provide an information for you for all above in our `Contribution Guidelines <https://github.com/titipata/pubmed_parser/blob/master/CONTRIBUTING.md>`_.
