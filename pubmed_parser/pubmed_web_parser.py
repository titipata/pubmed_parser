import sys
import re
import time
import requests
from lxml import etree
from lxml import html
from unidecode import unidecode

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from .utils import stringify_children

__all__ = ["parse_xml_web", "parse_citation_web", "parse_outgoing_citation_web"]


def load_xml(pmid, sleep=None):
    """
    Load XML file from given pmid from eutils site
    return a dictionary for given pmid and xml string from the site

    Parameters
    ----------
    pmid: (int, str)
        String of integer of a PMID

    sleep: int
        how much time we want to wait until requesting new xml
        default: None

    Return
    ------
    tree: Element
        An eutils XML of a given PMID
    """
    link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id={}".format(
        pmid
    )
    page = requests.get(link)
    tree = html.fromstring(page.content)
    if sleep is not None:
        time.sleep(sleep)
    return tree


def parse_pubmed_web_tree(tree):
    """
    Giving a tree Element from eutils, return parsed dictionary from the tree

    Parameters
    ----------
    tree: Element
        An lxml Element parsed from eutil website

    Return
    ------
    dict_out: dict
        A parsed output in dictionary format, dictionary keys includes 
        'title', 'abstract', 'journal', 'affliation' (string of affiliation with ';' separated),
        'authors' (string with ';' separated),
        'keywords' (keywords and MeSH terms from an XML -- if MeSH term it will be 'MeSH descriptor':'MeSH name')
        'doi', 'pii', 'year', 'language', 'version_id', 'version_date'
    """
    if len(tree.xpath("//articletitle")) != 0:
        title = " ".join([title.text for title in tree.xpath("//articletitle")])
    elif len(tree.xpath("//booktitle")) != 0:
        title = " ".join([title.text for title in tree.xpath("//booktitle")])
    else:
        title = ""

    abstract_tree = tree.xpath("//abstract/abstracttext")
    abstract = " ".join([stringify_children(a).strip() for a in abstract_tree])

    if len(tree.xpath("//article//title")) != 0:
        journal = ";".join([t.text.strip() for t in tree.xpath("//article//title")])
    else:
        journal = ""

    pubdate = tree.xpath('//pubmeddata//history//pubmedpubdate[@pubstatus="medline"]')
    pubdatebook = tree.xpath(
        '//pubmedbookdata//history//pubmedpubdate[@pubstatus="medline"]'
    )
    if len(pubdate) >= 1 and pubdate[0].find("year") is not None:
        year = pubdate[0].find("year").text
    elif len(pubdatebook) >= 1 and pubdatebook[0].find("year") is not None:
        year = pubdatebook[0].find("year").text
    else:
        year = ""

    affiliations = list()
    if tree.xpath("//affiliationinfo/affiliation") is not None:
        for affil in tree.xpath("//affiliationinfo/affiliation"):
            affiliations.append(affil.text)
    affiliations_text = "; ".join(affiliations)

    authors_tree = tree.xpath("//authorlist/author")
    authors = list()
    if authors_tree is not None:
        for a in authors_tree:
            firstname = (
                a.find("forename").text if a.find("forename") is not None else ""
            )
            lastname = a.find("lastname").text if a.find("forename") is not None else ""
            fullname = (firstname + " " + lastname).strip()
            if fullname == "":
                fullname = (
                    a.find("collectivename").text
                    if a.find("collectivename") is not None
                    else ""
                )
            authors.append(fullname)
        authors_text = "; ".join(authors)
    else:
        authors_text = ""

    keywords = ""
    keywords_mesh = tree.xpath("//meshheadinglist//meshheading")
    keywords_book = tree.xpath("//keywordlist//keyword")
    if len(keywords_mesh) > 0:
        mesh_terms_list = []
        for m in keywords_mesh:
            keyword = (
                m.find("descriptorname").attrib.get("ui", "")
                + ":"
                + m.find("descriptorname").text
            )
            mesh_terms_list.append(keyword)
        keywords = ";".join(mesh_terms_list)
    elif len(keywords_book) > 0:
        keywords = ";".join([m.text or "" for m in keywords_book])
    else:
        keywords = ""

    doi = tree.xpath('//elocationid[@eidtype="doi"]')
    try:
        doi = doi[0].text
    except IndexError:
        doi = None

    pii = tree.xpath('//elocationid[@eidtype="pii"]')
    try:
        pii = pii[0].text
    except IndexError:
        pii = None

    language = tree.xpath("//language")
    try:
        language = language[0].text
    except IndexError:
        language = None
    
    medline_citation = tree.xpath('//medlinecitation')
    try:
        version_id = medline_citation[0].attrib.get('versionid')
        version_date = medline_citation[0].attrib.get('versiondate')
    except IndexError:
        version_id, version_date = None, None

    dict_out = {
        "title": title,
        "abstract": abstract,
        "journal": journal,
        "affiliation": affiliations_text,
        "authors": authors_text,
        "keywords": keywords,
        "doi": doi,
        "pii": pii,
        "year": year,
        "language": language,
        "version_id": version_id,
        "version_date": version_date,
    }
    return dict_out


def parse_xml_web(pmid, sleep=None, save_xml=False):
    """
    Give an input PMID, load and parse XML using PubMed eutils

    Parameters
    ----------
    pmid: str
        A string of PMID which you want to parse from eutils    
    sleep: int
        An integer of how long you want to wait after parsing one PMID from eutils
        default: None
    save_xml: bool
        if it is True, save an XML output as a string in the key ``xml`` in an output dictionary.
        It is good to check the information in 
        if it is False, we won't save a full XML to an output
        default: False

    Return
    ------
    dict_out: dict
        A dictionary contains information of parsed XML from a given PMID

    Examples
    --------
    >>> pubmed_parser.parse_xml_web(11360989, sleep=1, save_xml=False)
    {
        'title': 'Molecular biology and evolution. Can genes explain biological complexity?',
        'abstract': '',
        'journal': 'Science (New York, N.Y.)',
        'affiliation': 'Collegium Budapest (Institute for Advanced Study), 2 Szentháromság u., H-1014 Budapest, Hungary. szathmary@colbud.hu',
        'authors': 'E Szathmáry; F Jordán; C Pál',
        'keywords': 'D000818:Animals;D005075:Biological Evolution;...',
        'doi': '10.1126/science.1060852',
        'year': '2001',
        'version_id': None,
        'version_date': None,
        'pmid': '11360989'
    }
    """
    tree = load_xml(pmid, sleep=sleep)
    dict_out = parse_pubmed_web_tree(tree)
    dict_out["pmid"] = str(pmid)
    if save_xml:
        dict_out["xml"] = etree.tostring(tree)
    return dict_out


def extract_citations(tree):
    """
    Extract number of citations from a given eutils XML tree.

    Parameters
    ----------
    tree: Element
        An lxml Element parsed from eutil website

    Return
    ------
    n_citations: int
        Number of citations that an article get until parsed date. If no citations found, return 0
    """
    citations_text = tree.xpath('//form/h2[@class="head"]/text()')[0]
    n_citations = re.sub("Is Cited by the Following ", "", citations_text).split(" ")[0]
    try:
        n_citations = int(n_citations)
    except:
        n_citations = 0
    return n_citations


def extract_pmc(citation):
    """
    Extract PMC from a given eutils XML tree.

    Parameters
    ----------
    tree: Element
        An lxml Element parsed from eutil website

    Return
    ------
    pmc: str
        PubMed Central ID (PMC) of an article
    """
    pmc_text = [c for c in citation.split("/") if c != ""][-1]
    pmc = re.sub("PMC", "", pmc_text)
    return pmc


def convert_document_id(doc_id, id_type="PMC"):
    """
    Convert a given document id to dictionary of other id.
    Please see http://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/ for more info

    Parameters
    ----------
    doc_id: (int, str)
        A string or integer of document ID
    id_type: str
        A document ID type corresponding to an input ``doc_id``
        default: 'PMC'
        options: 'PMID', 'DOI', or 'OTHER'

    Return
    ------
    output_dict: dict
        A dictionary contains possible mapping of a given document ID including 'pmc', 'pmid', and 'doi'.
        If the document ID cannot be found, this will return empty string instead

    Examples
    --------
    >>> pubmed_parser.pubmed_web_parser.convert_document_id(6933944, id_type='PMC')
    {'pmc': 'PMC6933944', 'pmid': '31624211', 'doi': '10.1126/science.aax1562'}
    """
    doc_id = str(doc_id)
    if id_type == "PMC":
        doc_id = "PMC{}".format(doc_id)
        pmc = doc_id
        convert_link = "http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids={}".format(
            doc_id
        )
    elif id_type in ["PMID", "DOI", "OTHER"]:
        convert_link = "http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids={}".format(
            doc_id
        )
    else:
        raise ValueError("Give id_type from PMC or PMID or DOI or OTHER")

    convert_page = requests.get(convert_link)
    convert_tree = html.fromstring(convert_page.content)
    record = convert_tree.find("record").attrib
    if "status" in record or "pmcid" not in record:
        raise ValueError("Cannot convert given document id to PMC")
    if id_type in ["PMID", "DOI", "OTHER"]:
        if "pmcid" in record:
            pmc = record["pmcid"]
        else:
            pmc = ""
    pmid = record["pmid"] if "pmid" in record else ""
    doi = record["doi"] if "doi" in record else ""
    return {"pmc": pmc, "pmid": pmid, "doi": doi}


def parse_citation_web(doc_id, id_type="PMC"):
    """
    Parse citations from given document id

    Parameters
    ----------
    doc_id: (str, int)
        document id
    id_type: str
        corresponding type of doc_id. This can be a choice from the following ['PMC', 'PMID', 'DOI', 'OTHER']

    Return
    ------
    dict_out: dict
        output is a dictionary contains following keys
        'pmc' (Pubmed Central ID), 'pmid' (Pubmed ID), 
        'doi' (DOI of an article),  'n_citations' (number of citations for given articles),
        'pmc_cited' (list of PMCs that cite the given PMC)

    Examples
    --------
    >>> pubmed_parser.parse_citation_web(6933944, id_type='PMC')
    {
        'n_citations': 0,
        'pmid': '31624211',
        'pmc': '6933944',
        'doi': '10.1126/science.aax1562',
        'pmc_cited': []
    }
    """
    assert id_type in ["PMC", "PMID", "DOI", "OTHER"]

    doc_id_dict = convert_document_id(doc_id, id_type=id_type)
    pmc = doc_id_dict["pmc"]
    link = "http://www.ncbi.nlm.nih.gov/pmc/articles/{}/citedby/".format(pmc)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    n_citations = extract_citations(tree)
    n_pages = int(n_citations / 30) + 1

    pmc_cited_all = list()  # all PMC cited
    citations = tree.xpath('//div[@class="rprt"]/div[@class="title"]/a/@href')[1::]
    pmc_cited = list(map(extract_pmc, citations))
    pmc_cited_all.extend(pmc_cited)
    if n_pages >= 2:
        for i in range(2, n_pages + 1):
            link = "http://www.ncbi.nlm.nih.gov/pmc/articles/{}/citedby/?page={}".format(
                pmc, i
            )
            page = requests.get(link)
            tree = html.fromstring(page.content)
            citations = tree.xpath('//div[@class="rprt"]/div[@class="title"]/a/@href')[
                1::
            ]
            pmc_cited = list(map(extract_pmc, citations))
            pmc_cited_all.extend(pmc_cited)
    pmc_cited_all = [p for p in pmc_cited_all if p is not pmc]
    dict_out = {
        "n_citations": n_citations,
        "pmid": doc_id_dict["pmid"],
        "pmc": re.sub("PMC", "", doc_id_dict["pmc"]),
        "doi": doc_id_dict["doi"],
        "pmc_cited": pmc_cited_all,
    }
    return dict_out


def parse_outgoing_citation_web(doc_id, id_type="PMC"):
    """
    A function to load citations from NCBI eutils API for a given document

    Example URL:
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pmc&linkname=pmc_refs_pubmed&id=221212

    Parameters
    ----------
    doc_id: str
        The document ID
    id_type: str
        A type of provided document ID, can be either 'PMC' or 'PMID'

    Return
    ------
    dict_out: dict
        a dictionary containing the following keys 'n_citations' (number of citations for that article),
        'doc_id' (the document ID number), 'id_type' (the type of document ID provided (PMCID or PMID)),
        'pmid_cited' (a list of papers cited by the document as PMIDs)

    >>> pubmed_parser.parse_outgoing_citation_web(6933944, id_type='PMC')
    {
        'n_citations': 11,
        'doc_id': '6933944',
        'id_type': 'PMC',
        'pmid_cited': ['30705152', ..., ]
    }
    """
    doc_id = str(doc_id)
    if id_type == "PMC":
        db = "pmc"
        linkname = "pmc_refs_pubmed"
    elif id_type == "PMID":
        db = "pubmed"
        linkname = "pubmed_pubmed_refs"
    else:
        raise ValueError("Unsupported id_type `{}`".format(id_type))
    link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom={}&linkname={}&id={}".format(
        db, linkname, doc_id
    )

    parser = etree.XMLParser()
    with urlopen(link) as f:
        tree = etree.parse(f, parser)
    pmid_cited_all = tree.xpath("/eLinkResult/LinkSet/LinkSetDb/Link/Id/text()")
    n_citations = len(pmid_cited_all)
    if not n_citations:  # If there are no citations, likely a bad doc_id
        return None
    dict_out = {
        "n_citations": n_citations,
        "doc_id": doc_id,
        "id_type": id_type,
        "pmid_cited": pmid_cited_all,
    }
    return dict_out
