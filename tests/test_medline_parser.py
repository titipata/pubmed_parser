import os
import pytest

import pubmed_parser as pp


def test_parse_medline_xml():
    """
    Test parse captions and figure ID from an XML file
    """
    parsed_xml = pp.parse_pubmed_xml(os.path.join('data', 'pone.0046493.nxml'))
    assert len(parsed_xml.get('abstract')) > 0
    assert len(parsed_xml.get('full_title')) > 0
    assert parsed_xml.get('pmc') == '3460867'
    assert parsed_xml.get('doi') == '10.1371/journal.pone.0046493'
