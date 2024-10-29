"""
Parsers for MEDLINE XML
"""
import re
import numpy as np
import gzip
from itertools import chain
from lxml import etree
from collections import defaultdict
from pubmed_parser.utils import read_xml, stringify_children, month_or_day_formater

__all__ = ["parse_medline_xml",  "parse_grant_id", "split_mesh"]


def parse_pmid(pubmed_article):
    """
    A function to parse PMID from a given Pubmed Article tree

    Parameters
    ----------
    pubmed_article: Element
        The lxml node pointing to a medline document

    Returns
    -------
    pmid: str
        A string of PubMed ID parsed from a given
    """
    medline = pubmed_article.find("MedlineCitation")
    if medline.find("PMID") is not None:
        pmid = medline.find("PMID").text
        return pmid
    else:
        article_ids = pubmed_article.find("PubmedData/ArticleIdList")
        if article_ids is not None:
            pmid = article_ids.find('ArticleId[@IdType="pmid"]')
            if pmid is not None:
                if pmid.text is not None:
                    pmid = pmid.text.strip()
                else:
                    pmid = ""
            else:
                pmid = ""
        else:
            pmid = ""
    return pmid


def parse_doi(pubmed_article):
    """
    A function to parse DOI from a given Pubmed Article tree

    Parameters
    ----------
    pubmed_article: Element
        The lxml node pointing to a medline document

    Returns
    -------
    doi: str
        A string of DOI parsed from a given ``pubmed_article``
    """
    medline = pubmed_article.find("MedlineCitation")
    article = medline.find("Article")
    elocation_ids = article.findall("ELocationID")

    if len(elocation_ids) > 0:
        for e in elocation_ids:
            doi = e.text.strip() or "" if e.attrib.get("EIdType", "") == "doi" else ""
    else:
        article_ids = pubmed_article.find("PubmedData/ArticleIdList")
        if article_ids is not None:
            doi = article_ids.find('ArticleId[@IdType="doi"]')
            doi = (
                (doi.text.strip() if doi.text is not None else "")
                if doi is not None
                else ""
            )
        else:
            doi = ""
    return doi


def parse_mesh_terms(medline, parse_subs=False):
    """
    A function to parse MESH terms from article

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document
    parse_subs: bool
        If True, parse mesh subterms as well.
    Returns
    -------
    mesh_terms: str
        String of semi-colon ``;`` spearated MeSH (Medical Subject Headings)
        terms contained in the document.
    """
    if parse_subs:
        return parse_mesh_terms_with_subs(medline)
    if medline.find("MeshHeadingList") is not None:
        mesh = medline.find("MeshHeadingList")
        mesh_terms_list = [
            m.find("DescriptorName").attrib.get("UI", "")
            + ":"
            + m.find("DescriptorName").text
            for m in mesh.getchildren()
        ]
        mesh_terms = "; ".join(mesh_terms_list)
    else:
        mesh_terms = ""
    return mesh_terms


def parse_mesh_terms_with_subs(medline):
    """
    A function to parse MESH terms and subterms from article

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document

    Returns
    -------
    mesh_terms: str
        String of semi-colon ``;`` spearated MeSH (Medical Subject Headings) terms contained in the document
        and mesh subterms concatenated " / "
        and appended with * if the subterm is a major topic.
    """
    if medline.find("MeshHeadingList") is not None:
        mesh = medline.find("MeshHeadingList")
        mesh_terms_list = []
        for m in mesh.getchildren():
            term = m.find("DescriptorName").attrib.get("UI", "") + ":" + \
                   m.find("DescriptorName").text
            if m.attrib.get("MajorTopicYN", "") == "Y":
                term += "*"
            for q in m.findall("QualifierName"):
                term += " / " + q.attrib.get("UI", "") + ":" + \
                        q.text
                if q.attrib.get("MajorTopicYN", "") == "Y":
                    term += "*"
            mesh_terms_list.append(term)
        mesh_terms = "; ".join(mesh_terms_list)
    else:
        mesh_terms = ""
    return mesh_terms


def split_mesh(mesh):
    """String split a string from parse_mesh_terms_with_subs()

    Parameters
    ----------
    mesh: str
        A string returned from parse_mesh_terms_with_subs()

    Returns
    -------
    mesh_list: List of List of 2-tuples of strings
        A list representation of the mesh headings

    Example
    --------
    # >>> pubmed_parser.split_mesh('D001249:Asthma / Q000188:drug therapy*; D001993:Bronchodilator Agents / Q000008:administration & dosage* / Q000009:adverse effects
')
    [[('D001249', 'Asthma'), ('Q000188', 'drug therapy*')],
     [('D001993', 'Bronchodilator Agents'), ('Q000008', 'administration & dosage*'), ('Q000009', 'adverse effects')]]
    """
    mesh_list = []
    for term in mesh.split("; "):
        subs = []
        for subterm in term.split(" / "):
            ui, descriptor = subterm.split(":")
            subs.append((ui, descriptor))
        mesh_list.append(subs)
    return mesh_list


def parse_publication_types(medline):
    """Parse Publication types from article

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document

    Returns
    -------
    publication_types: str
        String of semi-colon spearated publication types
    """
    publication_types = []
    publication_type_list = medline.find("Article/PublicationTypeList")
    if publication_type_list is not None:
        publication_type_list = publication_type_list.findall("PublicationType")
        for publication_type in publication_type_list:
            publication_types.append(
                publication_type.attrib.get("UI", "")
                + ":"
                + (publication_type.text.strip() or "")
            )
    publication_types = "; ".join(publication_types)
    return publication_types


def parse_keywords(medline):
    """Parse keywords from article, separated by ;

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document

    Returns
    -------
    keywords: str
        String of concatenated keywords.
    """
    keyword_list = medline.find("KeywordList")
    keywords = list()
    if keyword_list is not None:
        for k in keyword_list.findall("Keyword"):
            if k.text is not None:
                keywords.append(k.text)
        keywords = "; ".join(keywords)
    else:
        keywords = ""
    return keywords


def parse_chemical_list(medline):
    """Parse chemical list from article

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document

    Returns
    -------
    chemical_list: str
        String of semi-colon spearated chemical list
    """
    chemical_list = []
    chemicals = medline.find("ChemicalList")
    if chemicals is not None:
        for chemical in chemicals.findall("Chemical"):
            substance_name = chemical.find("NameOfSubstance")
            chemical_list.append(
                substance_name.attrib.get("UI", "")
                + ":"
                + (substance_name.text.strip() or "")
            )
    chemical_list = "; ".join(chemical_list)
    return chemical_list


def parse_other_id(medline):
    """Parse OtherID from article, each separated by ;

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document

    Returns
    -------
    other_id: str
        String of semi-colon separated Other IDs found in the document
    """
    pmc = ""
    other_id = list()
    oids = medline.findall("OtherID")
    if oids is not None:
        for oid in oids:
            if "PMC" in oid.text:
                pmc = oid.text
            else:
                other_id.append(oid.text)
        other_id = "; ".join(other_id)
    else:
        other_id = ""
    return {"pmc": pmc, "other_id": other_id}


def parse_journal_info(medline):
    """Parse MEDLINE journal information

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document

    Returns
    -------
    dict_out: dict
        dictionary with keys including `medline_ta`, `nlm_unique_id`,
        `issn_linking` and `country`
    """
    journal_info = medline.find("MedlineJournalInfo")
    if journal_info is not None:
        if journal_info.find("MedlineTA") is not None:
            medline_ta = (
                journal_info.find("MedlineTA").text or ""
            )  # equivalent to Journal name
        else:
            medline_ta = ""
        if journal_info.find("NlmUniqueID") is not None:
            nlm_unique_id = journal_info.find("NlmUniqueID").text or ""
        else:
            nlm_unique_id = ""
        if journal_info.find("ISSNLinking") is not None:
            issn_linking = journal_info.find("ISSNLinking").text
        else:
            issn_linking = ""
        if journal_info.find("Country") is not None:
            country = journal_info.find("Country").text or ""
        else:
            country = ""
    else:
        medline_ta = ""
        nlm_unique_id = ""
        issn_linking = ""
        country = ""
    dict_info = {
        "medline_ta": medline_ta.strip(),
        "nlm_unique_id": nlm_unique_id,
        "issn_linking": issn_linking,
        "country": country,
    }
    return dict_info


def parse_grant_id(pubmed_article):
    """Parse Grant ID and related information from a given MEDLINE tree

    Parameters
    ----------
    pubmed_article: Element
        The lxml node pointing to a medline document

    Returns
    -------
    grant_list: list
        List of grants acknowledged in the publications. Each
        entry in the dictionary contains the PubMed ID,
        grant ID, grant acronym, country, and agency.
    """
    medline = pubmed_article.find("MedlineCitation")
    article = medline.find("Article")

    grants = article.find("GrantList")
    grant_list = list()
    if grants is not None:
        grants_list = grants.getchildren()
        for grant in grants_list:
            grant_country = grant.find("Country")
            if grant_country is not None:
                country = grant_country.text
            else:
                country = ""
            grant_agency = grant.find("Agency")
            if grant_agency is not None:
                agency = grant_agency.text
            else:
                agency = ""
            grant_acronym = grant.find("Acronym")
            if grant_acronym is not None:
                acronym = grant_acronym.text
            else:
                acronym = ""
            grant_id = grant.find("GrantID")
            if grant_id is not None:
                gid = grant_id.text
            else:
                gid = ""
            grant_dict = {
                "grant_id": gid,
                "grant_acronym": acronym,
                "country": country,
                "agency": agency,
            }
            grant_list.append(grant_dict)
    return grant_list


def parse_author_affiliation(medline):
    """Parse MEDLINE authors and their corresponding affiliations

    Parameters
    ----------
    medline: Element
        The lxml node pointing to a medline document

    Returns
    -------
    authors: list
        List of authors and their corresponding affiliation in dictionary format
    """
    authors = []
    article = medline.find("Article")
    if article is not None:
        author_list = article.find("AuthorList")
        if author_list is not None:
            authors_list = author_list.findall("Author")
            for author in authors_list:
                if author.find("ForeName") is not None:
                    forename = (author.find("ForeName").text or "").strip() or ""
                else:
                    forename = ""
                if author.find("Initials") is not None:
                    initials = (author.find("Initials").text or "").strip() or ""
                else:
                    initials = ""
                if author.find("LastName") is not None:
                    lastname = (author.find("LastName").text or "").strip() or ""
                else:
                    lastname = ""
                if author.find("Identifier") is not None:
                    identifier = (author.find("Identifier").text or "").strip() or ""
                else:
                    identifier = ""
                if author.find("AffiliationInfo/Affiliation") is not None:
                    affiliation = list(chain(*([c.text] for c in author.findall("AffiliationInfo/Affiliation")))) or []
                    affiliation = [
                        c.replace(
                            "For a full list of the authors' affiliations please see the Acknowledgements section.",
                            "",
                        ) for c in affiliation
                    ]
                    affiliation = "|".join(affiliation)
                else:
                    affiliation = ""
                authors.append(
                    {
                        "lastname": lastname,
                        "forename": forename,
                        "initials": initials,
                        "identifier": identifier,
                        "affiliation": affiliation,
                    }
                )
    return authors


def date_extractor(journal, year_info_only):
    """Extract PubDate information from an Article in the Medline dataset.

    Parameters
    ----------
    journal: Element
        The 'Journal' field in the Medline dataset
    year_info_only: bool
        if True, this tool will only attempt to extract year information from PubDate.
        if False, an attempt will be made to harvest all available PubDate information.
        If only year and month information is available, this will yield a date of
        the form 'YYYY-MM'. If year, month and day information is available,
        a date of the form 'YYYY-MM-DD' will be returned.

    Returns
    -------
    PubDate: str
        PubDate extracted from an article.
        Note: If year_info_only is False and a month could not be
        extracted this falls back to year automatically.
    """
    day = None
    month = None
    issue = journal.xpath("JournalIssue")[0]
    issue_date = issue.find("PubDate")

    if issue_date.find("Year") is not None:
        year = issue_date.find("Year").text
        if not year_info_only:
            if issue_date.find("Month") is not None:
                month = month_or_day_formater(issue_date.find("Month").text)
                if issue_date.find("Day") is not None:
                    day = month_or_day_formater(issue_date.find("Day").text)
    elif issue_date.find("MedlineDate") is not None:
        year_text = issue_date.find("MedlineDate").text
        year = re.findall(r"\d{4}", year_text)
        if len(year) >= 1:
            year = year[0]
        else:
            year = ""
    else:
        year = ""

    if year_info_only or month is None:
        return year
    else:
        return "-".join(str(x) for x in filter(None, [year, month, day]))


def parse_references(pubmed_article, reference_list):
    """Parse references from Pubmed Article

    Parameter
    ---------
    pubmed_article: Element
        The lxml element pointing to a medline document

    reference_list: bool
        if it is True, return a list of dictionary
        if it is False return a string of PMIDs seprated by semicolon ';'

    Return
    ------
    references: (list, str)
        if 'reference_list' is set to True, return a list of dictionary
        if 'reference_list' is set to False return a string of PMIDs seprated by semicolon ';'
    """
    references = []
    reference_list_data = pubmed_article.find("PubmedData/ReferenceList")
    if reference_list_data is not None:
        for ref in reference_list_data.findall("Reference"):
            citation = ref.find("Citation")
            if citation is not None:
                if citation.text is not None:
                    citation = citation.text.strip()
                else:
                    citation = ""
            else:
                citation = ""
            article_ids = ref.find("ArticleIdList")
            pmid = (
                article_ids.find('ArticleId[@IdType="pubmed"]')
                if article_ids is not None
                else None
            )
            if pmid is not None:
                if pmid.text is not None:
                    pmid = pmid.text.strip()
                else:
                    pmid = ""
            else:
                pmid = ""
            references.append({"citation": citation, "pmid": pmid})

    if reference_list:
        return references
    else:
        references = ";".join(
            [ref["pmid"] for ref in references if ref["pmid"] != ""]
        )
        return references


def parse_article_info(
    pubmed_article, year_info_only, nlm_category, author_list, reference_list, parse_subs=False
):
    """Parse article nodes from Medline dataset

    Parameters
    ----------
    pubmed_article: Element
        The lxml element pointing to a medline document
    year_info_only: bool
        see more details in date_extractor()
    nlm_category: bool
        see more details in parse_medline_xml()
    author_list: bool
        if True, return output as list, else
    reference_list: bool
        if True, parse reference list as an output
    parse_subs: bool
        if True, parse mesh terms with subterms
    Returns
    -------
    article: dict
        Dictionary containing information about the article, including
        `title`, `abstract`, `journal`, `authors`, `affiliations`, `pubdate`,
        `pmid`, `other_id`, `mesh_terms`, `pages`, `issue`, and `keywords`. The field
        `delete` is always `False` because this function parses
        articles that by definition are not deleted.
    """
    medline = pubmed_article.find("MedlineCitation")
    article = medline.find("Article")

    if article.find("ArticleTitle") is not None:
        title = stringify_children(article.find("ArticleTitle")).strip() or ""
    else:
        title = ""

    if article.find("Journal/JournalIssue/Volume") is not None:
        volume = article.find("Journal/JournalIssue/Volume").text or ""
    else:
        volume = ""

    if article.find("Language") is not None:
        languages = ";".join([language.text for language in article.findall("Language")])
    else:
        languages = ""

    if article.find("VernacularTitle") is not None:
        vernacular_title = stringify_children(article.find("VernacularTitle")).strip() or ""
    else:
        vernacular_title = ""

    if article.find("Journal/JournalIssue/Issue") is not None:
        issue = article.find("Journal/JournalIssue/Issue").text or ""
    else:
        issue = ""

    if volume == "":
        issue = ""
    else:
        issue = f"{volume}({issue})"

    if article.find("Pagination/MedlinePgn") is not None:
        pages = article.find("Pagination/MedlinePgn").text or ""
    else:
        pages = ""

    category = "NlmCategory" if nlm_category else "Label"
    if article.find("Abstract/AbstractText") is not None:
        # parsing structured abstract
        if len(article.findall("Abstract/AbstractText")) > 1:
            abstract_list = list()
            for abstract in article.findall("Abstract/AbstractText"):
                section = abstract.attrib.get(category, "")
                if section != "UNASSIGNED":
                    abstract_list.append("\n")
                    abstract_list.append(abstract.attrib.get(category, ""))
                section_text = stringify_children(abstract).strip()
                abstract_list.append(section_text)
            abstract = "\n".join(abstract_list).strip()
        else:
            abstract = (
                stringify_children(article.find("Abstract/AbstractText")).strip() or ""
            )
    elif article.find("Abstract") is not None:
        abstract = stringify_children(article.find("Abstract")).strip() or ""
    else:
        abstract = ""

    authors_dict = parse_author_affiliation(medline)
    if not author_list:
        affiliations = ";".join(
            [
                author.get("affiliation", "")
                for author in authors_dict
                if author.get("affiliation", "") != ""
            ]
        )
        authors = ";".join(
            [
                author.get("lastname", "") + "|" + author.get("forename", "") + "|" +
                author.get("initials", "") + "|" + author.get("identifier", "")
                for author in authors_dict
            ]
        )
    else:
        authors = authors_dict
    journal = article.find("Journal")
    journal_name = " ".join(journal.xpath("Title/text()"))

    pmid = parse_pmid(pubmed_article)
    doi = parse_doi(pubmed_article)
    references = parse_references(pubmed_article, reference_list)
    pubdate = date_extractor(journal, year_info_only)
    mesh_terms = parse_mesh_terms(medline, parse_subs=parse_subs)
    publication_types = parse_publication_types(medline)
    chemical_list = parse_chemical_list(medline)
    keywords = parse_keywords(medline)
    other_id_dict = parse_other_id(medline)
    journal_info_dict = parse_journal_info(medline)
    dict_out = {
        "title": title,
        "issue": issue,
        "pages": pages,
        "abstract": abstract,
        "journal": journal_name,
        "authors": authors,
        "pubdate": pubdate,
        "pmid": pmid,
        "mesh_terms": mesh_terms,
        "publication_types": publication_types,
        "chemical_list": chemical_list,
        "keywords": keywords,
        "doi": doi,
        "references": references,
        "delete": False,
        "languages": languages,
        "vernacular_title": vernacular_title
    }
    if not author_list:
        dict_out.update({"affiliations": affiliations})
    dict_out.update(other_id_dict)
    dict_out.update(journal_info_dict)
    return dict_out


def parse_medline_xml(
    path,
    year_info_only=True,
    nlm_category=False,
    author_list=False,
    reference_list=False,
    parse_downto_mesh_subterms=False
):
    """Parse XML file from Medline XML format available at
    https://ftp.ncbi.nlm.nih.gov/pubmed/
    
    
    Parameters
    ----------
    path: str
        The path
    year_info_only: bool
        if True, this tool will only attempt to extract year information from PubDate.
        if False, an attempt will be made to harvest all available PubDate information.
        If only year and month information is available, this will yield a date of
        the form 'YYYY-MM'. If year, month and day information is available,
        a date of the form 'YYYY-MM-DD' will be returned.
        NOTE: the resolution of PubDate information in the Medline(R) database varies
        between articles.
        default: True
    nlm_category: bool
        if True, this will parse structured abstract where each section if original Label
        if False, this will parse structured abstract where each section will be assigned to
        NLM category of each sections
        default: False
    author_list: bool
        if True, return parsed author output as a list of authors
        if False, return parsed author output as a string of authors concatenated with ``;``
        default: False
    reference_list: bool
        if True, parse reference list as an output
        if False, return string of PMIDs concatenated with ;
        default: False
    parse_downto_mesh_subterms: bool
        if True, return mesh terms concatenated with "; " and mesh subterms concatenated " / "
                and appended with * if the subterm is major
        if False, return mesh_terms concatenated with "; "
        default: False

    Return
    ------
    An iterator of dictionary containing information about articles in NLM format.
        see `parse_article_info`). Articles that have been deleted will be
        added with no information other than the field `delete` being `True`

    Examples
    --------
    >>> article_iterator = pubmed_parser.parse_medline_xml('data/pubmed20n0014.xml.gz')
    >>> for article in article_iterator:
    ...     print(article['title'])
    """
    with gzip.open(path, "rb") as f:
        for event, element in etree.iterparse(f, events=("end",)):
            if element.tag == "PubmedArticle":
                res = parse_article_info(
                    element,
                    year_info_only,
                    nlm_category,
                    author_list,
                    reference_list,
                    parse_subs=parse_downto_mesh_subterms
                )
                res['grant_ids'] = parse_grant_id(element)
                element.clear()
                yield res
