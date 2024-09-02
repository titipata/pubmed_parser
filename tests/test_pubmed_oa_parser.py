import os
import tarfile
from io import BytesIO
import requests
import pubmed_parser as pp

def fetch_pubmed_xml(db_dir):
    """Fetch Pubmed OA XML package"""
    url = f'https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/{db_dir}.tar.gz'
    response = requests.get(url)
    tar_data = BytesIO(response.content)
    with tarfile.open(fileobj=tar_data, mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith('.nxml'):
                file_content = tar.extractfile(member)
                content = file_content.read()
                return content

# Get up-to-date pubmed online article
pubmed_dir = {"3460867": "00/00/PMC3460867",
              "28298962": "8e/71/PMC5334499",
              "9539395": "51/b3/PMC9539395",
              "1280406": "5f/92/PMC1280406",
              "30443433": "6f/c7/PMC6218202"
              }
pubmed_xml_3460867 = fetch_pubmed_xml(pubmed_dir['3460867'])
pubmed_xml_1280406 = fetch_pubmed_xml(pubmed_dir['1280406'])
pubmed_xml_30443433 = fetch_pubmed_xml(pubmed_dir['30443433'])


pubmed_xml_9539395 = fetch_pubmed_xml(pubmed_dir['9539395'])
captions_9539395 = pp.parse_pubmed_caption(pubmed_xml_9539395)


def test_parse_pubmed_xml():
    """
    Test parsing metadata from a PubMed XML file
    """
    parsed_xml = pp.parse_pubmed_xml(pubmed_xml_3460867)
    assert isinstance(parsed_xml, dict)
    assert len(parsed_xml.get("abstract")) > 0
    assert len(parsed_xml.get("full_title")) > 0
    assert parsed_xml.get("pmc") == "3460867"
    assert parsed_xml.get("doi") == "10.1371/journal.pone.0046493"
    assert parsed_xml.get("subjects") == "Research Article; Biology; Biochemistry; Enzymes; Enzyme Metabolism; Lipids; Fatty Acids; Glycerides; Lipid Metabolism; Neutral Lipids; Metabolism; Lipid Metabolism; Proteins; Globular Proteins; Protein Classes; Recombinant Proteins; Biotechnology; Microbiology; Bacterial Pathogens; Bacteriology; Emerging Infectious Diseases; Host-Pathogen Interaction; Microbial Growth and Development; Microbial Metabolism; Microbial Pathogens; Microbial Physiology; Proteomics; Sequence Analysis; Spectrometric Identification of Proteins"  # noqa
    assert "Competing Interests: " in parsed_xml.get("coi_statement")
    assert parsed_xml.get("journal") == "PLoS ONE"
    assert parsed_xml.get('publication_year') == 2012
    assert parsed_xml.get('publication_date') == '01-01-2012'
    assert parsed_xml.get('epublication_date') == '28-9-2012'

    parsed_1280406 = pp.parse_pubmed_xml(pubmed_xml_1280406)
    assert parsed_1280406.get('publication_year') == 2005
    assert parsed_1280406.get('publication_date') == "01-9-2005"
    assert parsed_1280406.get('epublication_date') == "31-5-2005"

    parsed_30443433 = pp.parse_pubmed_xml(pubmed_xml_30443433)
    assert parsed_30443433.get('publication_year') is None
    assert parsed_30443433.get('publication_date') == "01-01"


def test_parse_pubmed_paragraph():
    """
    Test parsing captions and figure ID from a PubMed XML file
    """
    paragraphs = pp.parse_pubmed_paragraph(pubmed_xml_3460867)
    assert isinstance(paragraphs, list)
    assert isinstance(paragraphs[0], dict)
    assert len(paragraphs) == 58, "Expected number of paragraphs to be 58"
    assert (
        len(paragraphs[0]["reference_ids"]) == 11
    ), "Expected number of references in the first paragraph to be 11"


def test_parse_pubmed_references():
    """
    Test parsing references from a PubMed XML file
    """
    references = pp.parse_pubmed_references(pubmed_xml_3460867)
    assert isinstance(references, list)
    assert isinstance(references[0], dict)
    assert len(references) == 58, "Expected references to have length of 29"

    references_9539395 = pp.parse_pubmed_references(pubmed_xml_9539395)
    assert references_9539395[0].get('pmid') == '36094679'


def test_parse_pubmed_table():
    """
    Test parsing table from PubMed XML file
    """
    table_9539395 = pp.parse_pubmed_table(pubmed_xml_9539395)
    expected_cols = ['Gene', 'Uninfected and untreated', 'Day 7 postinoculation', 'PBS', 'sACE22.v2.4-IgG1']
    assert table_9539395[0].get('table_columns') == expected_cols


def test_parse_pubmed_caption():
    """
    Test parsing captions and figure ID from a PubMed XML file
    """
    captions = pp.parse_pubmed_caption(pubmed_xml_3460867)
    assert isinstance(captions, list)
    assert isinstance(captions[0], dict)
    assert (
        len(captions) == 4
    ), "Expected number of figures/captions to have a length of 4"


def test_parse_pubmed_caption_content():
    """This is a test for the caption content."""
    fig_caption = 'Aerosol delivery of sACE22.v2.4‐IgG1 alleviates lung injury and improves survival of SARS‐CoV‐2 gamma variant infected K18‐hACE2 transgenic mice \n\n'
    assert captions_9539395[0]['fig_caption'] == fig_caption
    assert captions_9539395[0]['fig_id'] == 'emmm202216109-fig-0001'
    assert captions_9539395[0]['fig_label'] == 'Figure 1'
    assert captions_9539395[8]['fig_label'] is None
    fig_list_items = [('A', 'K18‐hACE2 transgenic mice were inoculated with SARS‐CoV‐2 isolate /Japan/TY7‐503/2021 (gamma variant) at 1\u2009×\u2009104 PFU. sACE22.v2.4‐IgG1 (7.5\u2009ml at 8.3\u2009mg/ml in PBS) was delivered to the mice by a nebulizer in 25\u2009min at 12\u2009h, 48\u2009h, and 84\u2009h postinoculation. PBS was aerosol delivered as control.'), ('B, C', 'Survival (B) and weight loss (C). N\u2009=\u200910 mice for each group. The P‐value of the survival curve by the Gehan–Breslow–Wilcoxon test is shown. Error bars for mouse weight are centered on the mean and show SEM.'), ('D', "Viral load in the lung was measured by RT–qPCR on Day 7. The mRNA expression levels of SARS‐CoV‐2 Spike, Nsp, and Rdrp are normalized to the housekeeping gene peptidylprolyl isomerase A (Ppia). Data are presented as mean\u2009±\u2009SEM, N\u2009=\u20094 mice per group. *P\u2009<\u20090.05 by the unpaired Student's t‐test with two‐sided."), ('E', "Cytokine expression levels of Tnfa, Ifng, Il1a, and Il1b were measured by RT–qPCR normalized by Ppia. Data are presented as mean\u2009±\u2009SEM, N\u2009=\u20094 mice per group. *P\u2009<\u20090.05 by the unpaired Student's t‐test with two‐sided."), ('F, G', 'Representative H&E staining of lung sections on Day 7 postinoculation for control PBS group (F) and inhalation of the sACE22.v2.4‐IgG1 group (G). Images at left are low magnifications. Boxed regions (black) are shown at higher magnification on the right. Lungs from 4 independent mice were sectioned, stained, and imaged.')]
    assert captions_9539395[0]['fig_list-items'] == fig_list_items
    assert captions_9539395[0]['graphic_ref'] == 'EMMM-14-e16109-g008'
    assert captions_9539395[8]['graphic_ref'] is None
    assert captions_9539395[0]['pmc'] == '9539395'
    assert captions_9539395[0]['pmid'] == '36094679'
