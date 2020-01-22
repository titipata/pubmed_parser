import os
import pytest

import pubmed_parser as pp


def test_parse_medline_xml():
    """
    Test parsing MEDLINE XML
    """
    expected_title = "Monitoring of bacteriological contamination and as"
    expected_abstract = "Two hundred and sixty nine beef, 230 sheep and 165"

    parsed_medline = pp.parse_medline_xml(os.path.join("data", "pubmed20n0014.xml.gz"))
    assert isinstance(parsed_medline, list)
    assert len(parsed_medline) == 30000, "Expect to have 30000 records"
    assert (
        len([p for p in parsed_medline if len(p["title"]) > 0]) == 30000
    ), "Expect every records to have title"
    assert parsed_medline[0]["title"][0:50] == expected_title
    assert parsed_medline[0]["abstract"][0:50] == expected_abstract
    assert parsed_medline[0]["pmid"] == "399296"
