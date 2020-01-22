=========
Resources
=========

Here are some useful resources for downloading data.


Links to download Pubmed and MEDLINE dataset
--------------------------------------------

Here are links for downloading PubMed OA and MEDLINE data

- PubMed Open-Access (OA) dataset is available at ``http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/``. Here is the `FTP link <ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/>`_ for downloading the bulk of dataset. You can check `oa_bulk folder <ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk//>`_ to see the full tar files.
- the MEDLINE XMLs are available here ``ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/``
- the MEDLINE XMLs weekly updates are available here ``ftp://ftp.nlm.nih.gov/nlmdata/.medlease/gz/``
- MEDLINE Document Type Definitions (DTDs) file is available at this `link <https://www.nlm.nih.gov/databases/dtd/>`_. We can use it to see available tags from a given MEDLINE XML.


Download PubMed OA figures
--------------------------

Here, we explain how to download PubMed OA figures corresponded to the parsed information

- In ``pubmed_parser``, you can use ``parse_pubmed_caption`` to parse figures (to be specific ``figure_id``) and captions corresponding to a manuscript. 
- To download the images corresponding to a given ``PMC`` or ``PMID``, you can download a CSV file from ``ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_file_list.csv`` first. - The file will have columns ``PMID``, ``Accession ID`` (``PMC``), and ``File`` where it looks something like ``oa_package/08/e0/PMC13900.tar.gz``.
- You can then download a tar file for a given ``PMID`` or ``PMC`` from ``ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/08/e0/PMC13900.tar.gz``. You can check out ``ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/`` to get all the access for tar files.


PMC Copyright Notice
--------------------

Wehn you use Pubmed Parser to parse information from the website, do not download them as a bulk. Your IP might get banned from doing it.
Please see copyright notice when you scrape data from website `here <https://www.ncbi.nlm.nih.gov/pmc/about/copyright/#copy-PMC/>`_.

Alternative implementation of MEDLINE parsers
---------------------------------------------

There are a few implementation to parse MEDLINE dataset. You can see below if you are interested to these alternative implementations.

- `MEDLINE Kung-Fu <http://fnl.es/medline-kung-fu.html/>`_ which uses `medic <https://github.com/fnl/medic/>`_ to parse MEDLINE to database 
- `MEDLINEXMLToJSON <https://github.com/ldbib/MEDLINEXMLToJSON/>`_ implemented in JavaScript

