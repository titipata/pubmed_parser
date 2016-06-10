from .utils import *
from itertools import chain

__all__ = [
    'parse_medline_xml',
    'parse_medline_grantid'
]

def parse_pmid(medline):
    """
    Parse PMID from article
    """
    if medline.find('PMID') is not None:
        pmid = medline.find('PMID').text
    else:
        pmid = ''
    return pmid


def parse_mesh_terms(medline):
    """
    Parse MESH terms from article
    """
    if medline.find('MeshHeadingList') is not None:
        mesh = medline.find('MeshHeadingList')
        mesh_terms_list = [m.find('DescriptorName').text for m in mesh.getchildren()]
        mesh_terms = '; '.join(mesh_terms_list)
    else:
        mesh_terms = ''
    return mesh_terms


def parse_keywords(medline):
    """
    Parse keywords from article, separated by ;
    """
    keyword_list = medline.find('KeywordList')
    keywords = list()
    if keyword_list is not None:
        for k in keyword_list.findall('Keyword'):
            keywords.append(k.text)
        keywords = '; '.join(keywords)
    else:
        keywords = ''
    return keywords


def parse_grant_id(medline):
    """
    Parse Grant ID and related information given MEDLINE tree
    """
    article = medline.find('Article')
    pmid = parse_pmid(medline)

    grants = article.find('GrantList')
    grants_dict = list()
    if grants is not None:
        grants_list = grants.getchildren()
        for grant in grants_list:
            grant_country = grant.find('Country')
            if grant_country is not None:
                country = grant_country.text
            else:
                country = ''
            grant_agency = grant.find('Agency')
            if grant_agency is not None:
                agency = grant_agency.text
            else:
                agency = ''
            grant_acronym = grant.find('Acronym')
            if grant_acronym is not None:
                acronym = grant_acronym.text
            else:
                acronym = ''
            grant_id = grant.find('GrantID')
            if grant_id is not None:
                gid = grant_id.text
            else:
                gid = ''
            dict_ = {'pmid': pmid,
                     'grant_id': gid,
                     'grant_acronym': acronym,
                     'country': country,
                     'agency': agency}
            grants_dict.append(dict_)
    return grants_dict


def parse_article_info(medline):
    """
    Parse article nodes from Medline dataset
    """
    article = medline.find('Article')

    if article.find('ArticleTitle') is not None:
        title = stringify_children(article.find('ArticleTitle'))
    else:
        title = ''

    if article.find('Abstract') is not None:
        abstract = stringify_children(article.find('Abstract'))
    else:
        abstract = ''

    if article.find('AuthorList') is not None:
        authors = article.find('AuthorList').getchildren()
        authors_info = list()
        affiliations_info = list()
        for author in authors:
            if author.find('Initials') is not None:
                firstname = author.find('Initials').text
            else:
                firstname = ''
            if author.find('LastName') is not None:
                lastname = author.find('LastName').text
            else:
                lastname = ''
            if author.find('AffiliationInfo/Affiliation') is not None:
                affiliation = author.find('AffiliationInfo/Affiliation').text
            else:
                affiliation = ''
            authors_info.append(firstname + ' ' + lastname)
            affiliations_info.append(affiliation)
        affiliations_info = join([a for a in affiliations_info if a is not ''])
        authors_info = '; '.join(authors_info)
    else:
        affiliations_info = ''
        authors_info = ''

    journal = article.find('Journal')
    journal_name = join(journal.xpath('Title/text()'))
    issue = journal.xpath('JournalIssue')[0]
    issue_date = issue.find('PubDate')
    if issue_date.find('Year') is not None:
        year = issue_date.find('Year').text
    elif issue_date.find('MedlineDate') is not None:
        year_text = issue_date.find('MedlineDate').text
        year = year_text.split(' ')[0]
    else:
        year = ''

    pmid = parse_pmid(medline)
    mesh_terms = parse_mesh_terms(medline)
    keywords = parse_keywords(medline)

    return {'title': title,
            'abstract': abstract,
            'journal': journal_name,
            'author': authors_info,
            'affiliation': affiliations_info,
            'year': year,
            'pmid': pmid,
            'mesh_terms': mesh_terms,
            'keywords': keywords,
            'delete': False}


def parse_medline_xml(path):
    """
    Parse XML file from Medline XML format
    available at ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/
    """
    tree = read_xml(path)
    medline_citations = tree.xpath('//MedlineCitationSet/MedlineCitation')
    dict_out = list(map(parse_article_info, medline_citations))
    delete_citations = tree.xpath('//DeleteCitation/PMID')
    dict_delete = \
        [
            {'title': None,
             'abstract': None,
             'journal': None,
             'author': None,
             'affiliation': None,
             'year': None,
             'pmid': p.text,
             'mesh_terms': None,
             'keywords': None,
             'delete': True
             } for p in delete_citations
            ]
    dict_out.extend(dict_delete)
    return dict_out


def parse_medline_grantid(path):
    """
    Parse grant id from Medline XML file
    """
    tree = read_xml(path)
    medline_citations = tree.xpath('//MedlineCitationSet/MedlineCitation')
    grant_id_list = list(map(parse_grant_id, medline_citations))
    grant_id_list = list(chain(*grant_id_list)) # flatten list
    return grant_id_list
