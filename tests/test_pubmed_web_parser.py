import pubmed_parser as pp
import random


def test_pubmed_web_parser_all_fields_content():
    """
    Test all fields in two concrete articles
    """
    expected = {
        38218666: {
            "title": "[Not Available].",
            "abstract": "",
            "journal": "Zeitschrift fur Evidenz, Fortbildung und Qualitat im Gesundheitswesen",
            "affiliation": "Sektion Versorgungsforschung und Rehabilitationsforschung, Institut für Medizinische Biometrie und Statistik, Universitätsklinikum Freiburg, Medizinische Fakultät, Albert-Ludwigs-Universität Freiburg, Freiburg, Deutschland. Electronic address: rieka.warth@uniklinik-freiburg.de.; Institut für Allgemeinmedizin, Universitätsklinikum Freiburg, Medizinische Fakultät, Albert-Ludwigs-Universität Freiburg, Freiburg, Deutschland.",
            "authors": "Rieka von der Warth; Isabelle Hempler",
            "keywords": "",
            "doi": "10.1016/j.zefq.2023.11.002",
            "pii": "S1865-9217(23)00212-X",
            "year": "2024",
            "language": "ger",
            "pmid": "38218666",
            "version_id": None,
            "version_date": None,
        },
        23340801: {
            "title": "E. coli as an all-rounder: the thin line between commensalism and pathogenicity.",
            "abstract": "Escherichia coli is a paradigm for a versatile bacterial species which comprises harmless commensal as well as different pathogenic variants with the ability to either cause intestinal or extraintestinal diseases in humans and many animal hosts. Because of this broad spectrum of lifestyles and phenotypes, E. coli is a well-suited model organism to study bacterial evolution and adaptation to different growth conditions and niches. The geno- and phenotypic diversity, however, also hampers risk assessment and strain typing. A marked genome plasticity is the key to the great variability seen in this species. Acquisition of genetic information by horizontal gene transfer, gene loss as well as other genomic modifications, like DNA rearrangements and point mutations, can constantly alter the genome content and thus the fitness and competitiveness of individual variants in certain niches. Specific gene subsets and traits have been correlated with an increased potential of E. coli strains to cause intestinal or extraintestinal disease. Intestinal pathogenic E. coli strains can be reliably discriminated from non-pathogenic, commensal, or from extraintestinal E. coli pathogens based on genome content and phenotypic traits. An unambiguous distinction of extraintestinal pathogenic E. coli and commensals is, nevertheless, not so easy, as strains with the ability to cause extraintestinal infection are facultative pathogens and belong to the normal flora of many healthy individuals. Here, we compare insights into phylogeny, geno-, and phenotypic traits of commensal and pathogenic E. coli. We demonstrate that the borderline between extraintestinal virulence and intestinal fitness can be blurred as improved adaptability and competitiveness may promote intestinal colonization as well as extraintestinal infection by E. coli.",
            "journal": "Current topics in microbiology and immunology",
            "affiliation": "Institute of Hygiene, University of Münster, Münster, Germany. andreas.leimbach@ukmuenster.de",
            "authors": "Andreas Leimbach; Jörg Hacker; Ulrich Dobrindt",
            "keywords": "D000818:Animals;D004926:Escherichia coli;D004927:Escherichia coli Infections;D023281:Genomics;D006801:Humans;D007413:Intestinal Mucosa;D007422:Intestines;D010802:Phylogeny;D013559:Symbiosis",
            "doi": "10.1007/82_2012_303",
            "pii": None,
            "year": "2013",
            "language": "eng",
            "pmid": "23340801",
            "version_id": None,
            "version_date": None,
        },
    }
    
    for article in expected:
        assert pp.parse_xml_web(article) == expected[article]

def test_pubmed_web_parser_all_fields_existence():
    """
    Test existence of expected fields in random (also empty) queries
    """
    random_id = random.randint(11111111, 99999999)
    expected_keys = [
        "title",
        "abstract",
        "journal",
        "affiliation",
        "authors",
        "keywords",
        "doi",
        "pii",
        "year",
        "language",
        "version_id",
        "version_date",
        "pmid",
    ]
    pubmed_dict = pp.parse_xml_web(random_id, save_xml=False)
    
    assert list(pubmed_dict.keys()) == expected_keys

def test_pubmed_web_parser_save_xml():
    """
    Test existence of xml field if `save_xml=True`
    """
    random_id = random.randint(11111111, 99999999)
    pubmed_dict = pp.parse_xml_web(random_id, save_xml=True)
    
    assert "xml" in pubmed_dict


def test_doi():
    """Test the correct parsing of the doi."""
    pubmed_dict = pp.parse_xml_web("32145645", save_xml=False)
    assert pubmed_dict['doi'] == "10.1016/j.ejmech.2020.112186"


def test_pii():
    """Test the correct parsing of the pii."""
    pubmed_dict = pp.parse_xml_web("32145645", save_xml=False)
    assert pubmed_dict['pii'] == "S0223-5234(20)30153-7"


def test_version():
    """Test the correct parsing of the version."""
    xml_20029612 = pp.parse_xml_web('20029612')
    assert xml_20029612['version_id'] == '4'
    assert xml_20029612['version_date'] == '2011/01/03'

    xml_21113338 = pp.parse_xml_web('21113338')
    assert xml_21113338['version_id'] == '3'
    assert xml_21113338['version_date'] is None
