import os
from lxml import etree
from lxml.etree import tostring
from itertools import chain
from .utils import *

__all__ = [
    'list_xml_path',
    'parse_pubmed_xml',
    'parse_pubmed_paragraph',
    'parse_pubmed_references',
    'parse_pubmed_caption'
]


def list_xml_path(path_dir):
    """
    List full xml path under given directory

    Parameters
    ----------
    path_dir: str, path to directory that contains xml or nxml file

    Returns
    -------
    path_list: list, list of xml or nxml file from given path
    """
    fullpath = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(path_dir)) for f in fn]
    path_list = [folder for folder in fullpath if os.path.splitext(folder)[-1] == ('.nxml' or '.xml')]
    return path_list


def zip_author(author):
    """
    Give a list of author and its affiliation keys
    in this following format
    [first_name, last_name, [key1, key2]]
    return [[first_name, last_name, key1], [first_name, last_name, key2]] instead
    """
    author_zipped = list(zip([[author[0], author[1]]] * len(author[-1]), author[-1]))
    return list(map(lambda x: x[0] + [x[-1]], author_zipped))


def flatten_zip_author(author_list):
    """
    Apply zip_author to author_list and flatten it
    """
    author_zipped_list = map(zip_author, author_list)
    return list(chain.from_iterable(author_zipped_list))


def parse_article_meta(tree):
    """
    Parse PMID, PMC and DOI from given article tree
    """
    article_meta = tree.find('//article-meta')
    pmid_node = article_meta.find('article-id[@pub-id-type="pmid"]')
    pmc_node = article_meta.find('article-id[@pub-id-type="pmc"]')
    pub_id_node = article_meta.find('article-id[@pub-id-type="publisher-id"]')
    doi_node = article_meta.find('article-id[@pub-id-type="doi"]')

    pmid = pmid_node.text if pmid_node is not None else ''
    pmc = pmc_node.text if pmc_node is not None else ''
    pub_id = pub_id_node.text if pub_id_node is not None else ''
    doi = doi_node.text if doi_node is not None else ''

    dict_article_meta = {'pmid': pmid,
                         'pmc': pmc,
                         'doi': doi,
                         'publisher_id': pub_id}

    return dict_article_meta


def parse_pubmed_xml(path, include_path=False):
    """
    Given single xml path, extract information from xml file
    and return parsed xml file in dictionary format.
    """
    tree = read_xml(path)

    tree_title = tree.find('//title-group/article-title')
    if tree_title is not None:
        title = [t for t in tree_title.itertext()]
        sub_title = tree.xpath('//title-group/subtitle/text()')
        title.extend(sub_title)
        title = [t.replace('\n', ' ').replace('\t', ' ') for t in title]
        full_title = ' '.join(title)
    else:
        full_title = ''

    try:
        abstracts = list()
        abstract_tree = tree.findall('//abstract')
        for a in abstract_tree:
            for t in a.itertext():
                text = t.replace('\n', ' ').replace('\t', ' ').strip()
                abstracts.append(text)
        abstract = ' '.join(abstracts)
    except:
        abstract = ''

    journal_node = tree.findall('//journal-title')
    if journal_node is not None:
        journal = ' '.join([j.text for j in journal_node])
    else:
        journal = ''

    dict_article_meta = parse_article_meta(tree)
    pub_year_node = tree.find('//pub-date/year')
    pub_year = pub_year_node.text if pub_year_node is not None else ''

    subjects_node = tree.findall('//article-categories//subj-group/subject')
    subjects = list()
    if subjects_node is not None:
        for s in subjects_node:
            subject = ' '.join([s_.strip() for s_ in s.itertext()]).strip()
            subjects.append(subject)
        subjects = '; '.join(subjects)
    else:
        subjects = ''

    # create affiliation dictionary
    affil_id = tree.xpath('//aff[@id]/@id')
    if len(affil_id) > 0:
        affil_id = list(map(str, affil_id))
    else:
        affil_id = ['']  # replace id with empty list

    affil_name = tree.xpath('//aff[@id]')
    affil_name_list = list()
    for e in affil_name:
        name = stringify_affiliation_rec(e)
        name = name.strip().replace('\n', ' ')
        affil_name_list.append(name)
    affiliation_list = [[idx, name] for idx, name in zip(affil_id, affil_name_list)]

    tree_author = tree.xpath('//contrib-group/contrib[@contrib-type="author"]')
    author_list = list()
    for author in tree_author:
        author_aff = author.findall('xref[@ref-type="aff"]')
        try:
            ref_id_list = [str(a.attrib['rid']) for a in author_aff]
        except:
            ref_id_list = ''
        try:
            author_list.append([author.find('name/surname').text,
                                author.find('name/given-names').text,
                                ref_id_list])
        except:
            author_list.append(['', '', ref_id_list])
    author_list = flatten_zip_author(author_list)

    dict_out = {'full_title': full_title.strip(),
                'abstract': abstract,
                'journal': journal,
                'pmid': dict_article_meta['pmid'],
                'pmc': dict_article_meta['pmc'],
                'doi': dict_article_meta['doi'],
                'publisher_id': dict_article_meta['publisher_id'],
                'author_list': author_list,
                'affiliation_list': affiliation_list,
                'publication_year': pub_year,
                'subjects': subjects}
    if include_path:
        dict_out['path_to_file'] = path
    return dict_out


def parse_references(tree):
    """
    Give a tree as an input,
    parse it to dictionary if ref-id and cited PMID
    """
    dict_article_meta = parse_article_meta(tree)
    pmid = dict_article_meta['pmid']
    pmc = dict_article_meta['pmc']

    references = tree.xpath('//ref-list/ref[@id]')
    dict_refs = list()
    for r in references:
        ref_id = r.attrib['id']
        for rc in r:
            if 'publication-type' in rc.attrib.keys():
                if rc.attrib.values() is not None:
                    journal_type = rc.attrib.values()[0]
                else:
                    journal_type = ''
                names = list()
                if rc.find('name') is not None:
                    for n in rc.findall('name'):
                        name = ' '.join([t.text for t in n.getchildren()][::-1])
                        names.append(name)
                elif rc.find('person-group') is not None:
                    for n in rc.find('person-group'):
                        name = ' '.join(n.xpath('given-names/text()') + n.xpath('surname/text()'))
                        names.append(name)
                try:
                    article_title = rc.findall('article-title')[0].text
                except:
                    article_title = ''
                try:
                    journal = rc.findall('source')[0].text
                except:
                    journal = ''
                try:
                    pmid_cited = rc.findall('pub-id[@pub-id-type="pmid"]')[0].text
                except:
                    pmid_cited = ''
                dict_ref = {'ref_id': ref_id,
                            'name': '; '.join(names),
                            'article_title': article_title,
                            'journal': journal,
                            'journal_type': journal_type,
                            'pmid': pmid,
                            'pmc': pmc,
                            'pmid_cited': pmid_cited}
                dict_refs.append(dict_ref)
    return dict_refs


def parse_pubmed_references(path):
    """
    Given path to xml file, parse all references
    from that PMID
    """
    tree = read_xml(path)
    dict_refs = parse_references(tree)
    return dict_refs


def parse_paragraph(tree, dict_refs):
    """
    Give tree and reference dictionary
    return dictionary of referenced paragraph, section that it belongs to,
    and its cited PMID
    """
    dict_article_meta = parse_article_meta(tree)
    pmid = dict_article_meta['pmid']
    pmc = dict_article_meta['pmc']

    paragraphs = tree.xpath('//body//p')
    dict_pars = list()
    for p in paragraphs:
        try:
            text = ' '.join(p.xpath('text()')) # text of the paragraph
        except:
            text = ''
        try:
            section = p.xpath('../title/text()')[0]
        except:
            section = ''

        # find the reference codes used in the paragraphs, can be compared with bibliogrpahy
        try:
            par_bib_refs = p.findall('.//xref[@ref-type="bibr"]')
            par_refs = list()
            for r in par_bib_refs:
                par_refs.append(r.xpath('@rid')[0])
        except:
            par_refs = ''

        # search bibliography for PubMed ID's of referenced articles
        try:
            pm_ids = list()
            for r in par_refs:
                r_ref = list(filter(lambda ref: ref['ref_id'] == r, dict_refs))
                if r_ref[0]['pmid'] != '':
                    pm_ids.append(r_ref[0]['pmid'])
        except:
            pm_ids = list()

        dict_par = {'pmc': pmc,
                    'pmid': pmid,
                    'references_code': par_refs,
                    'references_pmids': pm_ids,
                    'section': section,
                    'text': text}
        dict_pars.append(dict_par)
    return dict_pars


def parse_pubmed_paragraph(path):
    """
    Given single xml path, extract information from xml file
    and return parsed xml file in dictionary format.
    """
    tree = read_xml(path)
    dict_refs = parse_references(tree)
    dict_pars = parse_paragraph(tree, dict_refs)
    return dict_pars


def parse_pubmed_caption(path):
    """
    Given single xml path, extract figure caption and
    reference id back to that figure
    """
    tree = read_xml(path)

    dict_article_meta = parse_article_meta(tree)
    pmid = dict_article_meta['pmid']
    pmc = dict_article_meta['pmc']

    figs = tree.findall('//fig')
    dict_captions = list()
    if figs is not None:
        for fig in figs:
            fig_id = fig.attrib['id']
            fig_label = stringify_children(fig.find('label'))
            fig_captions = fig.find('caption').getchildren()
            caption = ' '.join([stringify_children(c) for c in fig_captions])
            graphic = fig.find('graphic')
            if graphic is not None:
                graphic_ref = graphic.attrib.values()[0]
            dict_caption = {'pmid': pmid,
                            'pmc': pmc,
                            'fig_caption': caption,
                            'fig_id': fig_id,
                            'fig_label': fig_label,
                            'graphic_ref': graphic_ref}
            dict_captions.append(dict_caption)
    if not dict_captions:
        dict_captions = None
    return dict_captions
