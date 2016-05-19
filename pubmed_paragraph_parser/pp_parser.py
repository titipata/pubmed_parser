import pubmed_parser as pp
from lxml import etree
import pandas as pd

def join(l):
    return ' '.join(l)

path_xml = pp.list_xml_path('ABData/articles.A-B/3_Biotech/')
result = pd.DataFrame()

for i in range(len(path_xml)):
    tree = etree.parse(path_xml[i])
    
    #find reference data
    references = tree.xpath('//ref-list/ref[@id]')
    dict_refs = list()
    for r in references:
        names = list()

        #added getting the reference ID, useful for finding which paragraphs use this citation
        ref_id = r.xpath('@id')[0]

        for n in r.findall('.//name'):
            name = join([t.text for t in n.getchildren()][::-1])
            names.append(name)
        try:
            article_title = r.findall('.//article-title')[0].text
        except:
            article_title = ''
        try:
            journal = r.findall('.//source')[0].text
        except:
            journal = ''
        try:
            pmid = r.findall('.//pub-id[@pub-id-type="pmid"]')[0].text
        except:
            pmid = ''
        dict_ref = {'ref_id':ref_id, 'name': names, 'article_title': article_title, 
                    'journal': journal, 'pmid': pmid}
        dict_refs.append(dict_ref)
        
    #get article information
    try:
        pmid = tree.xpath('//article-meta/article-id[@pub-id-type="pmid"]')[0].text
    except:
        pmid = ''
    try:
        pmc = tree.xpath('//article-meta/article-id[@pub-id-type="pmc"]')[0].text
    except:
        pmc = ''
        
    #create paragraph data
    paragraphs = tree.xpath('//body//p')    
    dict_pars = list()
    for p in paragraphs:

        #get the text of the paragraph
        try:
            text = join(p.xpath('text()'))
        except:
            text = ''

        #get the name of the section the paragraph sits in
        try:
            location = p.xpath('../title/text()')[0]        
        except:
            location = ''

        #find the reference codes used in the paragraphs, can be compared with bibliogrpahy
        try:
            par_bib_refs = p.findall('.//xref[@ref-type="bibr"]')
            par_refs = list()
            for r in par_bib_refs:
                par_refs.append(r.xpath('@rid')[0])
        except:
            par_refs = ''

        #search bibliography for PubMed ID's of referenced articles
        try:
            pm_ids = list() 
            for r in par_refs:
                r_ref = filter(lambda ref: ref['ref_id'] == r, dict_refs)
                if r_ref[0]['pmid'] != '':
                    pm_ids.append(r_ref[0]['pmid'])
        except:
            pm_ids = ''

        dict_par = {'pmc':pmc, 'pmid': pmid, 'text':text, 'references': par_refs, 'ref_pm_ids':pm_ids, 'section': location}
        dict_pars.append(dict_par)
    
    d = pd.DataFrame(dict_pars)
    result = pd.concat([d, result])