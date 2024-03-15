import os
import pytest
import requests
import gzip
from io import BytesIO

import pubmed_parser as pp
from pubmed_parser import split_mesh

def fetch_compressed_pubmed_xml(pubmed_id):
    """Fetch up-to-date pubmed XML and return as compressed XML"""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={pubmed_id}"
    response = requests.get(url)
    if response.status_code == 200:
        compressed_stream = gzip.compress(response.content)
        compressed_stream = BytesIO(compressed_stream)
        return compressed_stream
    else:
        raise requests.exceptions.HTTPError(response.status_code)

# Get up-to-date medline XML
pubmed_ids = ['36400559', '28786991']
pubmed_ids_str = ','.join(pubmed_ids)
medline_compressed_stream = fetch_compressed_pubmed_xml(pubmed_ids_str)
# Parse
parsed_medline = pp.parse_medline_xml(medline_compressed_stream)
parsed_medline = list(parsed_medline)
article_36400559 = parsed_medline[0]
article_28786991 = parsed_medline[1]


def test_current_36400559():
    """This test checks all the expected fields from 36400559"""
    assert article_36400559['title'] == 'Back Pain: Differential Diagnosis and Management.'
    assert article_36400559['issue'] == '41(1)'
    assert article_36400559['pages'] == '61-76'
    assert article_36400559['abstract'] == 'Back pain is a common condition affecting millions of individuals each year. A biopsychosocial approach to back pain provides the best clinical framework. A detailed history and physical examination with a thorough workup are required to exclude emergent or nonoperative etiologies of back pain. The treatment of back pain first uses conventional therapies including lifestyle modifications, nonsteroidal anti-inflammatory drugs, physical therapy, and cognitive behavioral therapy. If these options have been exhausted and pain persists for greater than 6 weeks, imaging and a specialist referral may be indicated.'
    assert article_36400559['journal'] == 'Neurologic clinics'
    assert article_36400559['authors'] == 'Gibbs|David|D|;McGahan|Ben G|BG|;Ropper|Alexander E|AE|;Xu|David S|DS|'
    assert article_36400559['pubdate'] == '2023'
    assert article_36400559['pmid'] == '36400559'
    assert article_36400559['mesh_terms'] == 'D006801:Humans; D017116:Low Back Pain; D003937:Diagnosis, Differential; D001416:Back Pain; D000894:Anti-Inflammatory Agents, Non-Steroidal; D015928:Cognitive Behavioral Therapy'
    assert article_36400559['publication_types'] == 'D016428:Journal Article; D016454:Review'
    assert article_36400559['chemical_list'] == 'D000894:Anti-Inflammatory Agents, Non-Steroidal'
    assert article_36400559['keywords'] == 'Back pain; Diagnosis; Management; Outpatient'
    assert article_36400559['doi'] == ''
    assert article_36400559['references'] == ''
    assert article_36400559['delete'] == False
    assert article_36400559['languages'] == 'eng'
    assert article_36400559['vernacular_title'] == ''
    assert article_36400559['affiliations'] == 'Department of Neurological Surgery, The Ohio State Wexner Medical Center, 410 West 10th Street, Columbus, OH 43210, USA; The Ohio State University College of Medicine, 370 West 9th street, Columbus, OH 43210, USA.;Department of Neurological Surgery, The Ohio State Wexner Medical Center, 410 West 10th Street, Columbus, OH 43210, USA.;Department of Neurological Surgery, Baylor College of Medicine, 1 Baylor Plaza, Houston, TX 77030, USA.;Department of Neurological Surgery, The Ohio State Wexner Medical Center, 410 West 10th Street, Columbus, OH 43210, USA; Department of Neurological Surgery, Baylor College of Medicine, 1 Baylor Plaza, Houston, TX 77030, USA. Electronic address: David.xu@osumc.edu.'
    assert article_36400559['pmc'] == ''
    assert article_36400559['other_id'] == ''
    assert article_36400559['medline_ta'] == 'Neurol Clin'
    assert article_36400559['nlm_unique_id'] == '8219232'
    assert article_36400559['issn_linking'] == '0733-8619'
    assert article_36400559['country'] == 'United States'
    assert len(article_36400559['grant_ids']) == 0


def test_current_28786991():
    """This test checks all the expected fields from 28786991"""
    assert article_28786991['pmid'] == '28786991'
    assert article_28786991['doi'] == '10.1371/journal.pone.0180707'
    assert article_28786991['references'] == '26536035;20142576;25734119;20972853;26180947;20697787;24669751;16333924;16357823;20014914;16826161;12484001;24922157;19622511;25810908;22825465;15623870;10667625;18763668;21653249;3088430;1528182;9114623;2786998;8808039;3789233;9358916;3706591;26423762;20853177;23907316;27780211;20577159;26371760;22157884;10881762'
    assert article_28786991['vernacular_title'] == ''
    assert article_28786991['pmc'] == ''
    assert article_28786991['other_id'] == ''
    assert len(article_28786991['grant_ids']) == 1


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
