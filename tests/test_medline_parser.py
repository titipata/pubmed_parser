from io import BytesIO
import os

import gzip
import requests

import pubmed_parser as pp


def fetch_compressed_medline_xml(pubmed_id):
    """Fetch up-to-date pubmed XML and return as compressed XML."""
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={pubmed_id}"
    response = requests.get(url)
    if response.status_code == 200:
        compressed_stream = gzip.compress(response.content)
        compressed_stream = BytesIO(compressed_stream)
        return compressed_stream
    else:
        raise requests.exceptions.HTTPError(response.status_code)


parsed_medline = pp.parse_medline_xml(fetch_compressed_medline_xml(['36400559', '28786991']))
parsed_medline = list(parsed_medline)
article_36400559 = parsed_medline[0]
article_28786991 = parsed_medline[1]


def test_abstract():
    """This is a test for the abstract field."""
    assert article_36400559['abstract'] == 'Back pain is a common condition affecting millions of individuals each year. A biopsychosocial approach to back pain provides the best clinical framework. A detailed history and physical examination with a thorough workup are required to exclude emergent or nonoperative etiologies of back pain. The treatment of back pain first uses conventional therapies including lifestyle modifications, nonsteroidal anti-inflammatory drugs, physical therapy, and cognitive behavioral therapy. If these options have been exhausted and pain persists for greater than 6\xa0weeks, imaging and a specialist referral may be indicated.'


def test_affiliations():
    """This is a test for the affiliations field."""
    affiliations_36400559 = 'Department of Neurological Surgery, The Ohio State Wexner Medical Center, 410 West 10th Street, Columbus, OH 43210, USA; The Ohio State University College of Medicine, 370 West 9th street, Columbus, OH 43210, USA.;Department of Neurological Surgery, The Ohio State Wexner Medical Center, 410 West 10th Street, Columbus, OH 43210, USA.;Department of Neurological Surgery, Baylor College of Medicine, 1 Baylor Plaza, Houston, TX 77030, USA.;Department of Neurological Surgery, The Ohio State Wexner Medical Center, 410 West 10th Street, Columbus, OH 43210, USA; Department of Neurological Surgery, Baylor College of Medicine, 1 Baylor Plaza, Houston, TX 77030, USA. Electronic address: David.xu@osumc.edu.'
    assert article_36400559['affiliations'] == affiliations_36400559
    affiliations_28786991 = 'Phillip R. Lee Institute for Health Policy Studies, University of California, San Francisco, San Francisco, California, United States of America.|Global Health Sciences, University of California, San Francisco, San Francisco, California, United States of America.|The Consortium for the Assessment of Prevention Economics (CAPE), University of California, San Francisco, San Francisco, California, United States of America.;Phillip R. Lee Institute for Health Policy Studies, University of California, San Francisco, San Francisco, California, United States of America.|The Consortium for the Assessment of Prevention Economics (CAPE), University of California, San Francisco, San Francisco, California, United States of America.;Phillip R. Lee Institute for Health Policy Studies, University of California, San Francisco, San Francisco, California, United States of America.|The Consortium for the Assessment of Prevention Economics (CAPE), University of California, San Francisco, San Francisco, California, United States of America.;Phillip R. Lee Institute for Health Policy Studies, University of California, San Francisco, San Francisco, California, United States of America.|Global Health Sciences, University of California, San Francisco, San Francisco, California, United States of America.|The Consortium for the Assessment of Prevention Economics (CAPE), University of California, San Francisco, San Francisco, California, United States of America.;Centers for Disease Control and Prevention, Division of Tuberculosis Elimination, Atlanta, Georgia, United States of America.;Phillip R. Lee Institute for Health Policy Studies, University of California, San Francisco, San Francisco, California, United States of America.|Global Health Sciences, University of California, San Francisco, San Francisco, California, United States of America.|The Consortium for the Assessment of Prevention Economics (CAPE), University of California, San Francisco, San Francisco, California, United States of America.'
    assert article_28786991['affiliations'] == affiliations_28786991


def test_authors():
    """This is a test for the authors field."""
    authors_36400559 = 'Gibbs|David|D|;McGahan|Ben G|BG|;Ropper|Alexander E|AE|;Xu|David S|DS|'
    assert article_36400559['authors'] == authors_36400559
    authors_28786991 = 'Malekinejad|Mohsen|M|0000-0002-5721-6764;Parriott|Andrea|A|;Viitanen|Amanda P|AP|;Horvath|Hacsi|H|;Marks|Suzanne M|SM|;Kahn|James G|JG|'
    assert article_28786991['authors'] == authors_28786991


def test_chemical_list():
    """This is a test for the chemical_list field."""
    assert article_36400559['chemical_list'] == 'D000894:Anti-Inflammatory Agents, Non-Steroidal'
    assert article_28786991['chemical_list'] == ''


def test_country():
    """This is a test for the country field."""
    assert article_36400559['country'] == 'United States'
    assert article_28786991['country'] == 'United States'


def test_delete():
    """This is a test for the delete field."""
    assert not article_36400559['delete']
    assert not article_28786991['delete']


def test_doi():
    """This is a test for the doi field."""
    assert article_36400559['doi'] == ''
    assert article_28786991['doi'] == '10.1371/journal.pone.0180707'


def test_grant_ids():
    """This is a test for the grant_ids field."""
    assert article_36400559['grant_ids'] == []
    grant_ids_28786991 = [{'grant_id': 'U38 PS004649', 'grant_acronym': 'PS', 'country': 'United States', 'agency': 'NCHHSTP CDC HHS'}]
    assert article_28786991['grant_ids'] == grant_ids_28786991


def test_issn_linking():
    """This is a test for the issn_linking field."""
    assert article_36400559['issn_linking'] == '0733-8619'
    assert article_28786991['issn_linking'] == '1932-6203'


def test_issue():
    """This is a test for the issue field."""
    assert article_36400559['issue'] == '41(1)'
    assert article_28786991['issue'] == '12(8)'


def test_journal():
    """This is a test for the journal field."""
    assert article_36400559['journal'] == 'Neurologic clinics'
    assert article_28786991['journal'] == 'PloS one'


def test_keywords():
    """This is a test for the keywords field."""
    assert article_36400559['keywords'] == 'Back pain; Diagnosis; Management; Outpatient'
    assert article_28786991['keywords'] == ''


def test_languages():
    """This is a test for the languages field."""
    assert article_36400559['languages'] == 'eng'
    assert article_28786991['languages'] == 'eng'


def test_medline_ta():
    """This is a test for the medline_ta field."""
    assert article_36400559['medline_ta'] == 'Neurol Clin'
    assert article_28786991['medline_ta'] == 'PLoS One'


def test_mesh_terms():
    """This is a test for the mesh_terms field."""
    mesh_terms_36400559 = 'D006801:Humans; D017116:Low Back Pain; D003937:Diagnosis, Differential; D001416:Back Pain; D000894:Anti-Inflammatory Agents, Non-Steroidal; D015928:Cognitive Behavioral Therapy'
    assert article_36400559['mesh_terms'] == mesh_terms_36400559
    mesh_terms_28786991 = 'D054242:Emigrants and Immigrants; D006801:Humans; D014376:Tuberculosis; D014481:United States'
    assert article_28786991['mesh_terms'] == mesh_terms_28786991


def test_nlm_unique_id():
    """This is a test for the nlm_unique_id field."""
    assert article_36400559['nlm_unique_id'] == '8219232'
    assert article_28786991['nlm_unique_id'] == '101285081'


def test_other_id():
    """This is a test for the other_id field."""
    assert article_36400559['other_id'] == ''
    assert article_28786991['other_id'] == ''


def test_pages():
    """This is a test for the pages field."""
    assert article_36400559['pages'] == '61-76'
    assert article_28786991['pages'] == 'e0180707'


def test_pmc():
    """This is a test for the pmc field."""
    assert article_36400559['pmc'] == ''
    assert article_28786991['pmc'] == ''


def test_pmid():
    """This is a test for the pmid field."""
    assert article_36400559['pmid'] == '36400559'
    assert article_28786991['pmid'] == '28786991'


def test_pubdate():
    """This is a test for the pubdate field."""
    assert article_36400559['pubdate'] == '2023'
    assert article_28786991['pubdate'] == '2017'


def test_publication_types():
    """This is a test for the publication_types field."""
    publication_types_36400559 = 'D016428:Journal Article; D016454:Review'
    assert article_36400559['publication_types'] == publication_types_36400559
    publication_types_28786991 = 'D016428:Journal Article; D017418:Meta-Analysis; D016454:Review; D000078182:Systematic Review'
    assert article_28786991['publication_types'] == publication_types_28786991


def test_references():
    """This is a test for the references field."""
    assert article_36400559['references'] == ''
    references_28786991 = '26536035;20142576;25734119;20972853;26180947;20697787;24669751;16333924;16357823;20014914;16826161;12484001;24922157;19622511;25810908;22825465;15623870;10667625;18763668;21653249;3088430;1528182;9114623;2786998;8808039;3789233;9358916;3706591;26423762;20853177;23907316;27780211;20577159;26371760;22157884;10881762'
    assert article_28786991['references'] == references_28786991


def test_title():
    """This is a test for the title field."""
    assert article_36400559['title'] == 'Back Pain: Differential Diagnosis and Management.'
    title_28786991 = 'Yield of community-based tuberculosis targeted testing and treatment in foreign-born populations in the United States: A systematic review.'
    assert article_28786991['title'] == title_28786991


def test_vernacular_title():
    """This is a test for the vernacular_title field."""
    assert article_36400559['vernacular_title'] == ''
    assert article_28786991['vernacular_title'] == ''


def test_parse_medline_xml():
    """
    Test parsing MEDLINE XML
    """
    expected_title = "Monitoring of bacteriological contamination and as"
    expected_abstract = "Two hundred and sixty nine beef, 230 sheep and 165"
    parsed_medline = pp.parse_medline_xml(os.path.join("data", "pubmed20n0014.xml.gz"))
    parsed_medline = list(parsed_medline)
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


def test_parse_medline_mesh_terms():
    """
    Test parsing MeSH headings from MEDLINE XML
    """
    headings = parsed_medline[0]["mesh_terms"]
    expected = """D006801:Humans
D017116:Low Back Pain
D003937:Diagnosis, Differential
D001416:Back Pain
D000894:Anti-Inflammatory Agents, Non-Steroidal
D015928:Cognitive Behavioral Therapy""".strip().replace("\n", "; ")
    print(headings)
    assert headings == expected


# def test_parse_medline_mesh_terms_with_sub():
#     """
#     Test parsing MeSH subheadings from MEDLINE XML
#     """
#     subheadings = parsed_medline[1]["mesh_terms"]
#     expected = """D000280:Administration, Inhalation
# D000293:Adolescent
# D000328:Adult
# D000368:Aged
# D001249:Asthma / Q000188:drug therapy*
# D001993:Bronchodilator Agents / Q000008:administration & dosage* / Q000009:adverse effects
# D019819:Budesonide / Q000008:administration & dosage* / Q000009:adverse effects
# D002648:Child
# D004311:Double-Blind Method
# D004334:Drug Administration Schedule
# D004338:Drug Combinations
# D005260:Female
# D005541:Forced Expiratory Volume
# D000068759:Formoterol Fumarate / Q000008:administration & dosage* / Q000009:adverse effects
# D005938:Glucocorticoids / Q000008:administration & dosage
# D006801:Humans
# D060046:Maintenance Chemotherapy
# D008297:Male
# D055118:Medication Adherence
# D008875:Middle Aged
# D011795:Surveys and Questionnaires
# D013726:Terbutaline / Q000008:administration & dosage* / Q000009:adverse effects
# D055815:Young Adult""".replace("\n", "; ")
#     assert subheadings == expected
#     mesh_list = pp.split_mesh(expected)
#     expected_split_mesh = [
#         [('D000280', 'Administration, Inhalation')],
#         [('D000293', 'Adolescent')],
#         [('D000328', 'Adult')], [('D000368', 'Aged')],
#         [('D001249', 'Asthma'), ('Q000188', 'drug therapy*')],
#         [('D001993', 'Bronchodilator Agents'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
#         [('D019819', 'Budesonide'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
#         [('D002648', 'Child')], [('D004311', 'Double-Blind Method')], [('D004334', 'Drug Administration Schedule')],
#         [('D004338', 'Drug Combinations')],
#         [('D005260', 'Female')],
#         [('D005541', 'Forced Expiratory Volume')],
#         [('D000068759', 'Formoterol Fumarate'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
#         [('D005938', 'Glucocorticoids'), ('Q000008', 'administration & dosage')],
#         [('D006801', 'Humans')],
#         [('D060046', 'Maintenance Chemotherapy')],
#         [('D008297', 'Male')],
#         [('D055118', 'Medication Adherence')],
#         [('D008875', 'Middle Aged')],
#         [('D011795', 'Surveys and Questionnaires')],
#         [('D013726', 'Terbutaline'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')],
#         [('D055815', 'Young Adult')]]
#     assert mesh_list == expected_split_mesh


def test_parse_medline_language():
    """
    Test if all publications have a language.
    """
    parsed_medline = pp.parse_medline_xml("./data/pubmed20n0014.xml.gz")
    parsed_medline_list = list(parsed_medline)
    assert all([item['languages'] != '' for item in parsed_medline_list])
