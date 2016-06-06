import requests
from lxml import etree
from lxml import html
from unidecode import unidecode
from .utils import *

__all__ = [
    'parse_xml_web'
]


def load_xml(pmid, sleep=None):
    """
    Load XML file from given pmid from eutils site
    return a dictionary for given pmid and xml string from the site
    sleep: how much time we want to wait until requesting new xml
    """
    link = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=" + str(pmid)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    if sleep is not None:
        time.sleep(sleep)
    dict_xml = {'pmid': str(pmid), 'xml': etree.tostring(tree)} # turn xml to string (easier to save later on)
    return dict_xml


def get_author_string(tree):
    authors = tree.xpath('//authorlist//author')
    authors_text = []
    for a in authors:
        firstname = a.find('forename').text
        lastname = a.find('lastname').text
        fullname = firstname + ' ' + lastname
        authors_text.append(fullname)
    return '; '.join(authors_text)


def get_year_string(tree):
    year = ''.join(tree.xpath('//pubmeddata//history//pubmedpubdate[@pubstatus="medline"]/year/text()'))
    return year


def get_abstract_string(tree):
    abstract = unidecode(stringify_children(tree.xpath('//abstract')[0]))
    return abstract


def get_affiliation_string(tree):
    """
    Get all affiliation string
    """
    affiliation = '; '.join([a for a in tree.xpath('//affiliationinfo//affiliation/text()')])
    return affiliation


def parse_xml_tree(tree):
    """
    Giving tree, return simple parsed information from the tree
    """
    try:
        title = ' '.join(tree.xpath('//articletitle/text()'))
    except:
        title = ''

    try:
        abstract = get_abstract_string(tree)
    except:
        abstract = ''

    try:
        journal = ' '.join(tree.xpath('//article//title/text()')).strip()
    except:
        journal = ''

    try:
        year = get_year_string(tree)
    except:
        year = ''

    try:
        affiliation = get_affiliation_string(tree)
    except:
        affiliation = ''

    try:
        authors = get_author_string(tree)
    except:
        authors = ''

    dict_out = {'title': title,
                'abstract': abstract,
                'journal': journal,
                'affiliation': affiliation,
                'authors': authors,
                'year': year}
    return dict_out


def parse_xml_web(pmid, sleep=None, save_xml=False):
    """
    Give pmid, load and parse xml from Pubmed eutils
    if save_xml is True, save xml output in dictionary
    """
    dict_xml = load_xml(pmid, sleep=None)
    tree = etree.fromstring(dict_xml['xml'])
    dict_out = parse_xml_tree(tree)
    dict_out['pmid'] = dict_xml['pmid']
    if save_xml:
        dict_out['xml'] = dict_xml['xml']
    return dict_out
