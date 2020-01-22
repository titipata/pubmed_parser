import os
import pytest

import pubmed_parser as pp


def test_parse_pubmed_xml():
    """
    Test parse captions and figure ID from an XML file
    """
    parsed_xml = pp.parse_pubmed_xml(os.path.join("data", "pone.0046493.nxml"))
    assert isinstance(parsed_xml, dict)
    assert len(parsed_xml.get("abstract")) > 0
    assert len(parsed_xml.get("full_title")) > 0
    assert parsed_xml.get("pmc") == "3460867"
    assert parsed_xml.get("doi") == "10.1371/journal.pone.0046493"


def test_parse_pubmed_caption():
    """
    Test parsing captions and figure ID from a PubMed XML file
    """
    paragraphs = pp.parse_pubmed_paragraph(os.path.join("data", "pone.0046493.nxml"))
    assert isinstance(paragraphs, list)
    assert isinstance(paragraphs[0], dict)
    assert len(paragraphs) == 29, "Expected number of paragraphs to be 29"
    assert (
        len(paragraphs[0]["reference_ids"]) == 11
    ), "Expected number of references in the first paragraph to be 11"


def test_parse_pubmed_references():
    """
    Test parsing references from a PubMed XML file
    """
    references = pp.parse_pubmed_references(os.path.join("data", "pone.0046493.nxml"))
    assert isinstance(references, list)
    assert isinstance(references[0], dict)
    assert len(references) == 29, "Expected references to have length of 29"


def test_parse_pubmed_():
    """
    Test parsing figures and captions from a PubMed XML file
    """
    captions = pp.parse_pubmed_caption(os.path.join("data", "pone.0046493.nxml"))
    assert isinstance(captions, list)
    assert isinstance(captions[0], dict)
    assert (
        len(captions) == 4
    ), "Expected number of figures/captions to have a length of 4"
