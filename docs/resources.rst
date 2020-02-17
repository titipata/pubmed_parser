=========
Resources
=========

Here are some useful resources for downloading MEDLINE and PubMed Open Access (PubMed OA) XML data.

Links to download PubMed OA and MEDLINE dataset
-----------------------------------------------

Below, we provide links for downloading PubMed OA and MEDLINE data

- `PubMed Open-Access (OA) <http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/>`_ dataset is available at ``http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/``. Here is the `FTP link <ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/>`_ for downloading the bulk of dataset. In the FTP link, you can go to `oa_bulk folder <ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/>`_ to see the full available tar files.
- the MEDLINE XMLs are available here ``ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/``
- the MEDLINE XMLs weekly updates are available here ``ftp://ftp.nlm.nih.gov/nlmdata/.medlease/gz/``
- MEDLINE Document Type Definitions (DTDs) file is available at this `link <https://www.nlm.nih.gov/databases/dtd/>`_. We can use it to see available tags from a given MEDLINE XML.


Download PubMed OA figures
--------------------------

Here, we explain how to download PubMed OA figures corresponded to the parsed information from ``parse_pubmed_caption`` function

- In ``pubmed_parser``, you can use ``parse_pubmed_caption`` to parse figures (to be specific ``figure_id``) and captions corresponding to a manuscript. 
- To download the images corresponding to a given ``PMC`` or ``PMID``, you can download a CSV file from ``ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_file_list.csv`` first. The file will have columns ``PMID``, ``Accession ID`` (``PMC``), and ``File``. In ``File`` column, you can see the path to download a tar file of an XML and corresponding figures in the following format ``oa_package/08/e0/PMC13900.tar.gz``.
- You can use the path to download a tar file for a given ``PMID`` or ``PMC`` in a following format: ``ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/08/e0/PMC13900.tar.gz``. If you want to download all the tar files, check out ``ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/`` to see all the files.


PMC Copyright Notice
--------------------

When you use Pubmed Parser to parse information from the website, do not download them as a bulk. Your IP might get banned from doing it.
Please see copyright notice when you scrape data from website `here <https://www.ncbi.nlm.nih.gov/pmc/about/copyright/#copy-PMC/>`_.

Alternative implementation of MEDLINE parsers
---------------------------------------------

There are a few implementation to parse MEDLINE dataset. You can see below if you are interested to these alternative implementations.

- `MEDLINE Kung-Fu <http://fnl.es/medline-kung-fu.html/>`_ which uses `medic <https://github.com/fnl/medic/>`_ to parse MEDLINE to database 
- `MEDLINEXMLToJSON <https://github.com/ldbib/MEDLINEXMLToJSON/>`_ implemented in JavaScript

