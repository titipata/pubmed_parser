import os
import pytest
import requests
import gzip

import pubmed_parser as pp
from pubmed_parser import split_mesh

def fetch_pubmed_xml(pubmed_id):
    """Fetch up-to-date pubmed XML"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={pubmed_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch XML data. Status code: {response.status_code}")
        return None

def save_xml_to_gz(xml_content, filename):
    """Save XML to geziped file"""
    with gzip.open(filename, 'wb') as f:
        f.write(xml_content)
    print(f"XML data saved as {filename}")

pubmed_ids = ['36400559', '2930949', '11446611', '28786991']
pubmed_ids_str = ','.join(pubmed_ids)
medline_xml = fetch_pubmed_xml(pubmed_ids_str)
save_xml_to_gz(medline_xml, f'./data/test_current_medline.xml.gz')


def test_current_medline_xml():
    """Test up-to-date MEDLINE XML"""
    expected_fields = [
        "title",
        "issue",
        "pages",
        "abstract",
        "journal",
        "authors",
        "pubdate",
        "pmid",
        "mesh_terms",
        "publication_types",
        "chemical_list",
        "keywords",
        "doi",
        "references",
        "delete",
        "languages",
        "vernacular_title",
        "affiliations",
        "pmc",
        "other_id",
        "medline_ta",
        "nlm_unique_id",
        "issn_linking",
        "country",
        "grant_ids",
    ]
    parsed_medline = pp.parse_medline_xml(
        os.path.join("data", f"test_current_medline.xml.gz")
    )
    parsed_medline = list(parsed_medline)
    medline_article = parsed_medline[0]
    assert expected_fields == list(medline_article.keys())

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
    assert parsed_medline[0]["issue"] == "50(2)"
    assert parsed_medline[0]["pages"] == "123-33"
    assert parsed_medline[0]["abstract"][0:50] == expected_abstract
    assert parsed_medline[0]["pmid"] == "399296"
    assert parsed_medline[0]["languages"] == "eng"
    assert parsed_medline[0]["vernacular_title"] == ""


def test_parse_medline_grant_id():
    """
    Test parsing grants from MEDLINE XML
    """
    grants = pp.parse_medline_grant_id(os.path.join("data", "pubmed20n0014.xml.gz"))
    assert isinstance(grants, list)
    assert isinstance(grants[0], dict)
    assert grants[0]["pmid"] == "399300"
    assert grants[0]["grant_id"] == "HL17731"
    assert len(grants) == 484, "Expect number of grants in a given file to be 484"

def test_parse_medline_mesh_terms():
    """
    Test parsing MeSH headings from MEDLINE XML
    """
    parsed_medline = pp.parse_medline_xml(os.path.join("data", "pubmed-29768149.xml"),
                                          parse_downto_mesh_subterms=False)
    headings = parsed_medline[0]["mesh_terms"]
    expected = """D000280:Administration, Inhalation
D000293:Adolescent
D000328:Adult
D000368:Aged
D001249:Asthma
D001993:Bronchodilator Agents
D019819:Budesonide
D002648:Child
D004311:Double-Blind Method
D004334:Drug Administration Schedule
D004338:Drug Combinations
D005260:Female
D005541:Forced Expiratory Volume
D000068759:Formoterol Fumarate
D005938:Glucocorticoids
D006801:Humans
D060046:Maintenance Chemotherapy
D008297:Male
D055118:Medication Adherence
D008875:Middle Aged
D011795:Surveys and Questionnaires
D013726:Terbutaline
D055815:Young Adult""".replace("\n", "; ")
    print(headings)
    assert headings == expected


def test_parse_medline_mesh_terms_with_sub():
    """
    Test parsing MeSH subheadings from MEDLINE XML
    """
    parsed_medline = pp.parse_medline_xml(os.path.join("data", "pubmed-29768149.xml"),
                                          parse_downto_mesh_subterms=True)
    subheadings = parsed_medline[0]["mesh_terms"]
    expected = """D000280:Administration, Inhalation
D000293:Adolescent
D000328:Adult
D000368:Aged
D001249:Asthma / Q000188:drug therapy*
D001993:Bronchodilator Agents / Q000008:administration & dosage* / Q000009:adverse effects
D019819:Budesonide / Q000008:administration & dosage* / Q000009:adverse effects
D002648:Child
D004311:Double-Blind Method
D004334:Drug Administration Schedule
D004338:Drug Combinations
D005260:Female
D005541:Forced Expiratory Volume
D000068759:Formoterol Fumarate / Q000008:administration & dosage* / Q000009:adverse effects
D005938:Glucocorticoids / Q000008:administration & dosage
D006801:Humans
D060046:Maintenance Chemotherapy
D008297:Male
D055118:Medication Adherence
D008875:Middle Aged
D011795:Surveys and Questionnaires
D013726:Terbutaline / Q000008:administration & dosage* / Q000009:adverse effects
D055815:Young Adult""".replace("\n", "; ")
    assert subheadings == expected

    mesh_list = pp.split_mesh(expected)
    expected_split_mesh = [
        [('D000280', 'Administration, Inhalation')],
        [('D000293', 'Adolescent')],
        [('D000328', 'Adult')], [('D000368', 'Aged')],
        [('D001249', 'Asthma'), ('Q000188', 'drug therapy*')],
        [('D001993', 'Bronchodilator Agents'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
        [('D019819', 'Budesonide'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
        [('D002648', 'Child')], [('D004311', 'Double-Blind Method')], [('D004334', 'Drug Administration Schedule')],
        [('D004338', 'Drug Combinations')],
        [('D005260', 'Female')],
        [('D005541', 'Forced Expiratory Volume')],
        [('D000068759', 'Formoterol Fumarate'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
        [('D005938', 'Glucocorticoids'), ('Q000008', 'administration & dosage')],
        [('D006801', 'Humans')],
        [('D060046', 'Maintenance Chemotherapy')],
        [('D008297', 'Male')],
        [('D055118', 'Medication Adherence')],
        [('D008875', 'Middle Aged')],
        [('D011795', 'Surveys and Questionnaires')],
        [('D013726', 'Terbutaline'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
        [('D055815', 'Young Adult')]]
    assert mesh_list == expected_split_mesh

def test_parse_medline_language():
    """
    Test if all publications have a language
    """
    parsed_medline = pp.parse_medline_xml("./data/pubmed20n0014.xml.gz")
    parsed_medline_list = list(parsed_medline)
    assert all([item['languages'] != '' for item in parsed_medline_list])
