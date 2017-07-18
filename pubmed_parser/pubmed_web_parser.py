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

__all__ = [
    'parse_xml_web',
    'parse_citation_web',
    'parse_outgoing_citation_web'
]


def load_xml(pmid, sleep=None):
    """
    Load XML file from given pmid from eutils site
    return a dictionary for given pmid and xml string from the site
    sleep: how much time we want to wait until requesting new xml
    """
    link = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=%s" % str(pmid)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    if sleep is not None:
        time.sleep(sleep)
    return tree


def parse_pubmed_web_tree(tree):
    """
    Giving tree, return simple parsed information from the tree
    """

    if tree.xpath('//articletitle') is not None:
        title = ' '.join([title.text for title in tree.xpath('//articletitle')])
    else:
        title = ''

    abstract_tree = tree.xpath('//abstract/abstracttext')
    abstract = ' '.join([stringify_children(a).strip() for a in abstract_tree])

    if tree.xpath('//article//title') is not None:
        journal = ';'.join([t.text.strip() for t in tree.xpath('//article//title')])
    else:
        journal = ''

    pubdate = tree.xpath('//pubmeddata//history//pubmedpubdate[@pubstatus="medline"]')
    if len(pubdate) >= 1 and pubdate[0].find('year') is not None:
        year = pubdate[0].find('year').text
    else:
        year = ''

    affiliations = list()
    if tree.xpath('//affiliationinfo/affiliation') is not None:
        for affil in tree.xpath('//affiliationinfo/affiliation'):
            affiliations.append(affil.text)
    affiliations_text = '; '.join(affiliations)

    authors_tree = tree.xpath('//authorlist/author')
    authors = list()
    if authors_tree is not None:
        for a in authors_tree:
            firstname = a.find('forename').text if a.find('forename') is not None else ''
            lastname = a.find('lastname').text if a.find('forename') is not None else ''
            fullname = (firstname + ' ' + lastname).strip()
            if fullname == '':
                fullname = a.find('collectivename').text if a.find('collectivename') is not None else ''
            authors.append(fullname)
        authors_text = '; '.join(authors)
    else:
        authors_text = ''

    dict_out = {'title': title,
                'abstract': abstract,
                'journal': journal,
                'affiliation': affiliations_text,
                'authors': authors_text,
                'year': year}
    return dict_out


def parse_xml_web(pmid, sleep=None, save_xml=False):
    """
    Give pmid, load and parse xml from Pubmed eutils
    if save_xml is True, save xml output in dictionary
    """
    tree = load_xml(pmid, sleep=sleep)
    dict_out = parse_pubmed_web_tree(tree)
    dict_out['pmid'] = str(pmid)
    if save_xml:
        dict_out['xml'] = etree.tostring(tree)
    return dict_out


def extract_citations(tree):
    """
    Extract number of citations from given tree
    """
    citations_text = tree.xpath('//form/h2[@class="head"]/text()')[0]
    n_citations = re.sub("Is Cited by the Following ", "", citations_text).split(' ')[0]
    try:
        n_citations = int(n_citations)
    except:
        n_citations = 0
    return n_citations


def extract_pmc(citation):
    pmc_text = [c for c in citation.split('/') if c is not ''][-1]
    pmc = re.sub('PMC', '', pmc_text)
    return pmc


def convert_document_id(doc_id, id_type='PMC'):
    """
    Convert document id to dictionary of other id
    see: http://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/ for more info
    """
    doc_id = str(doc_id)
    if id_type == 'PMC':
        doc_id = 'PMC%s' % doc_id
        pmc = doc_id
        convert_link = 'http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids=%s' % doc_id
    elif id_type in ['PMID', 'DOI', 'OTHER']:
        convert_link = 'http://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=my_tool&email=my_email@example.com&ids=%s' % doc_id
    else:
        raise ValueError('Give id_type from PMC or PMID or DOI or OTHER')

    convert_page = requests.get(convert_link)
    convert_tree = html.fromstring(convert_page.content)
    record = convert_tree.find('record').attrib
    if 'status' in record or 'pmcid' not in record:
        raise ValueError('Cannot convert given document id to PMC')
    if id_type in ['PMID', 'DOI', 'OTHER']:
        if 'pmcid' in record:
            pmc = record['pmcid']
        else:
            pmc = ''
    return {'pmc': pmc,
            'pmid': record['pmid'] if 'pmid' in record else '',
            'doi': record['doi'] if 'doi' in record else ''}


def parse_citation_web(doc_id, id_type='PMC'):
    """
    Parse citations from given document id

    Parameters
    ----------
    doc_id: str or int, document id
    id_type: str from ['PMC', 'PMID', 'DOI', 'OTHER']

    Returns
    -------
    dict_out: dict, contains following keys
        pmc: Pubmed Central ID
        pmid: Pubmed ID
        doi: DOI of the article
        n_citations: number of citations for given articles
        pmc_cited: list of PMCs that cite the given PMC
    """

    doc_id_dict = convert_document_id(doc_id, id_type=id_type)
    pmc = doc_id_dict['pmc']
    link = "http://www.ncbi.nlm.nih.gov/pmc/articles/%s/citedby/" % pmc
    page = requests.get(link)
    tree = html.fromstring(page.content)
    n_citations = extract_citations(tree)
    n_pages = int(n_citations/30) + 1

    pmc_cited_all = list() # all PMC cited
    citations = tree.xpath('//div[@class="rprt"]/div[@class="title"]/a/@href')[1::]
    pmc_cited = list(map(extract_pmc, citations))
    pmc_cited_all.extend(pmc_cited)
    if n_pages >= 2:
        for i in range(2, n_pages+1):
            link = "http://www.ncbi.nlm.nih.gov/pmc/articles/%s/citedby/?page=%s" % (pmc, str(i))
            page = requests.get(link)
            tree = html.fromstring(page.content)
            citations = tree.xpath('//div[@class="rprt"]/div[@class="title"]/a/@href')[1::]
            pmc_cited = list(map(extract_pmc, citations))
            pmc_cited_all.extend(pmc_cited)
    pmc_cited_all = [p for p in pmc_cited_all if p is not pmc]
    dict_out = {'n_citations': n_citations,
                'pmid': doc_id_dict['pmid'],
                'pmc': re.sub('PMC', '', doc_id_dict['pmc']),
                'doi': doc_id_dict['doi'],
                'pmc_cited': pmc_cited_all}
    return dict_out


def parse_outgoing_citation_web(doc_id, id_type='PMC'):
    """
    Load citations from NCBI eutils API for a given document,
    return a dictionary containing:
        n_citations: number of citations for that article
        doc_id: the document ID number
        id_type: the type of document ID provided (PMCID or PMID)
        pmid_cited: list of papers cited by the document as PMIDs
    """
    doc_id = str(doc_id)
    if id_type is 'PMC':
        db = 'pmc'
        linkname = 'pmc_refs_pubmed'
    elif id_type is 'PMID':
        db = 'pubmed'
        linkname = 'pubmed_pubmed_refs'
    else:
        raise ValueError('Unsupported id_type `%s`' % id_type)
    link = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=%s&linkname=%s&id=%s' % (db, linkname, doc_id)

    parser = etree.XMLParser()
    with urlopen(link) as f:
        tree = etree.parse(f, parser)
    pmid_cited_all = tree.xpath('/eLinkResult/LinkSet/LinkSetDb/Link/Id/text()')
    n_citations = len(pmid_cited_all)
    if not n_citations: # If there are no citations, likely a bad doc_id
        return None
    dict_out = {'n_citations': n_citations,
                'doc_id': doc_id,
                'id_type': id_type,
                'pmid_cited': pmid_cited_all}
    return dict_out
