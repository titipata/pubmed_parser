import os
import numpy as np
import pandas as pd
from lxml import etree
from itertools import chain


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
    """
    parts = ([node.text] +
             list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
             [node.tail])
    return ''.join(filter(None, parts))


def extract_pubmed_xml(xmlpath, min_doc_len=0, min_abstract_len=0, max_abstract_len=10000):
    """
    Given single xml path, extract information from xml file
    and return a list
    """
    try:
        tree = etree.parse(xmlpath)
    except:
        try:
            tree = etree.fromstring(xmlpath)
        except:
            raise Exception("It was not able to read a path, a file-like object, or a string as an XML")

    len_doc = len(etree.tostring(tree).split())
    if len_doc >= min_doc_len:
        article_name = os.path.split(xmlpath)[-1]
        try:
            title = ' '.join(tree.xpath('//title-group/article-title/text()')).replace('\n', ' ')
            sub_title = ' '.join(tree.xpath('//title-group/subtitle/text()')).replace('\n', ' ').replace('\t', ' ')
            topic = title + ' ' + sub_title
        except:
            topic = ''
        try:
            abstract = ' '.join(tree.xpath('//abstract//text()'))
        except:
            abstract = ''
        try:
            journal_title = tree.xpath('//journal-title-group/journal-title')[0].text
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

        # discard if abstract length is to short or too long
        len_abstract = len(abstract.split())
        if len_abstract > max_abstract_len or len_abstract < min_abstract_len:
            return None

        # create affiliation dictionary
        aff_id = tree.xpath('//aff/@id')
        if len(aff_id) == 0:
            aff_id = ['']  # replace id with empty list

        aff_name = tree.xpath('//aff')
        aff_name_list = []
        for node in aff_name:
            aff_name_list.append(stringify_children(node))
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

        list_out = [article_name, topic, abstract, journal_title, pmid, pmc, pub_id, all_aff, aff_dict, pub_year]
        return list_out
