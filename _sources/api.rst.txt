API Documentation
=================

.. currentmodule:: pubmed_parser

The core functionality of Pubmed Parse can be divided into 3 main parts based on the source of the data we use an as input.
Input source can be either from MEDLINE XML, PubMed Open Access subset (PubMed OA), or Website (using eutils).
Below, we list the core APIs implemented in Pubmed Parser

Parse MEDLINE XML 
-----------------

.. autofunction:: parse_medline_xml
.. autofunction:: parse_grant_id

Parse PubMed OA XML
-------------------

.. autofunction:: parse_pubmed_xml
.. autofunction:: parse_pubmed_references
.. autofunction:: parse_pubmed_paragraph
.. autofunction:: parse_pubmed_caption
.. autofunction:: parse_pubmed_table

Parse from Website
------------------

.. autofunction:: parse_xml_web
.. autofunction:: parse_citation_web
.. autofunction:: parse_outgoing_citation_web
