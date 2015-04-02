import os
import pandas as pd
from lxml import etree
from itertools import chain
from functools import partial
from operator import is_not
from lxml.etree import tostring
from compiler.ast import flatten

__all__ = [
    'list_xmlpath',
    'parse_pubmed_xml',
    'create_pubmed_df',
    'pretty_print_xml',
]


def list_xmlpath(path_init):
    """
    List full xml path under given directory
    """
    fullpath = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path_init)) for f in fn]
    xmlpath_list = [folder for folder in fullpath if os.path.splitext(folder)[-1] == ('.nxml' or '.xml')]
    return xmlpath_list


def stringify_children(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = ([node.text] +
             list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
             [node.tail])
    return ''.join(filter(None, parts))


def stringify_affiliation(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = ([node.text] +
             list(chain(*([c.text if (c.tag != 'label' and c.tag !='sup') else '', c.tail] for c in node.getchildren()))) +
             [node.tail])
    return ' '.join(filter(None, parts))


def recur_children(node):
    """
    Recursive through node to when it has multiple children
    """
    if len(node.getchildren()) == 0:
        parts = ([node.text or ''] + [node.tail or '']) if (node.tag != 'label' and node.tag !='sup') else ([node.tail or ''])
        return parts
    else:
        parts = ([node.text or ''] +
                 [recur_children(c) for c in node.getchildren()] +
                 [node.tail or ''])
        return parts


def stringify_affiliation_rec(node):
    """
    Flatten and join list to string
    ref: http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    """
    parts = recur_children(node)
    return ' '.join(flatten(parts)).strip()


def parse_pubmed_xml(xmlpath):
    """
    Given single xml path, extract information from xml file
    and return as a list
    """
    try:
        tree = etree.parse(xmlpath)
    except:
        try:
            tree = etree.fromstring(xmlpath)
        except:
            raise Exception("It was not able to read a path, a file-like object, or a string as an XML")

    try:
        title = ' '.join(tree.xpath('//title-group/article-title/text()')).replace('\n', ' ')
        sub_title = ' '.join(tree.xpath('//title-group/subtitle/text()')).replace('\n', ' ').replace('\t', ' ')
        full_title = title + ' ' + sub_title
    except:
        full_title = ''
    try:
        abstract = ' '.join(tree.xpath('//abstract//text()'))
    except:
        abstract = ''
    try:
        journal_title = tree.xpath('//journal-title-group/journal-title')[0].text
    except:
        try:
            journal_title = tree.xpath('/article/front/journal-meta/journal-title/text()')[0]
        except:
            journal_title = ''
    try:
        pmid = tree.xpath('//article-meta/article-id[@pub-id-type="pmid"]')[0].text
    except:
        pmid = ''
    try:
        pmc = tree.xpath('//article-meta/article-id[@pub-id-type="pmc"]')[0].text
    except:
        pmc = ''
    try:
        pub_id = tree.xpath('//article-meta/article-id[@pub-id-type="publisher-id"]')[0].text
    except:
        pub_id = ''
    try:
        pub_year = tree.xpath('//pub-date/year/text()')[0]
    except:
        pub_year = ''
    try:
        subjects = ','.join(tree.xpath('//article-categories//subj-group//text()'))
    except:
        subjects = ''

    # create affiliation dictionary
    aff_id = tree.xpath('//aff[@id]/@id')
    if len(aff_id) == 0:
        aff_id = ['']  # replace id with empty list

    aff_name = tree.xpath('//aff[@id]')
    aff_name_list = []
    for node in aff_name:
        aff_name_list.append(stringify_affiliation_rec(node))
    aff_dict = dict(zip(aff_id, map(lambda x: x.strip().replace('\n', ' '), aff_name_list)))  # create dictionary

    tree_author = tree.xpath('//contrib-group/contrib[@contrib-type="author"]')
    all_aff = []
    for el in tree_author:
        el0 = el.findall('xref[@ref-type="aff"]')
        try:
            rid_list = [tmp.attrib['rid'] for tmp in el0]
        except:
            rid_list = ''
        try:
            all_aff.append([el.find('name/surname').text, el.find('name/given-names').text, rid_list])
        except:
            all_aff.append(['', '', rid_list])

    list_out = {'full_title': full_title.strip(),
                'abstract': abstract,
                'journal_title': journal_title,
                'pmid': pmid,
                'pmc': pmc,
                'publisher_id': pub_id,
                'author_list': all_aff,
                'affiliation_list': aff_dict,
                'publication_year': pub_year,
                'subjects': subjects}
    return list_out


def create_pubmed_df(path_list, remove_abs=False, path_xml=False):
    """
    Given list of xml paths, return parsed DataFrame

    path_list: list of xml paths
    remove_abs: if true, remove row of dataframe if parsed xml contains no abstract
    path_xml: if true, concat path to xml file when constructing DataFrame
    """
    pm_docs = []
    for path in path_list:
        pm_dict = parse_pubmed_xml(path)
        if path_xml:
            pm_dict['path_to_file'] = path
        pm_docs.append(pm_dict)

    pm_docs = filter(partial(is_not, None), pm_docs)  # remove None
    pm_docs_df = pd.DataFrame(pm_docs) # turn to pandas DataFrame

    # remove empty abstract
    if remove_abs:
        pm_docs_df = pm_docs_df[pm_docs_df.abstract != ''].reset_index().drop('index', axis=1)

    # reorder columns
    if path_xml:
        pm_docs_df = pm_docs_df[['full_title',
                                 'abstract',
                                 'journal_title',
                                 'pmid',
                                 'pmc',
                                 'publisher_id',
                                 'author_list',
                                 'affiliation_list',
                                 'publication_year',
                                 'subjects',
                                 'path_to_file']]
    else:
        pm_docs_df = pm_docs_df[['full_title',
                                 'abstract',
                                 'journal_title',
                                 'pmid',
                                 'pmc',
                                 'publisher_id',
                                 'author_list',
                                 'affiliation_list',
                                 'publication_year',
                                 'subjects']]

    return pm_docs_df


def pretty_print_xml(xmlpath):
    """Given a XML path, file-like, or string, print a pretty xml version of it"""
    try:
        tree = etree.parse(xmlpath)
    except:
        try:
            tree = etree.fromstring(xmlpath)
        except:
            raise Exception("It was not able to read a path, a file-like object, or a string as an XML")

    print tostring(tree, pretty_print=True)


def chunks(l, n):
    """
    Yield successive n-sized chunks from l
    Suppose we want to chunk all path list into smaller chunk
    example: chunks(path_list, 10000)
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
