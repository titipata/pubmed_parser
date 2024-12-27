import calendar
from itertools import chain
from time import strptime

from collections.abc import Iterable

from lxml import etree
from six import string_types


def remove_namespace(tree):
    """
    Strip namespace from parsed XML
    """
    for node in tree.iter():
        try:
            has_namespace = node.tag.startswith("{")
        except AttributeError:
            continue  # node.tag is not a string (node is a comment or similar)
        if has_namespace:
            node.tag = node.tag.split("}", 1)[1]


def read_xml(path, nxml=False):
    """
    Parse tree from given XML path
    """
    try:
        tree = etree.parse(path)
        if ".nxml" in path or nxml:
            remove_namespace(tree)  # strip namespace when reading an XML file
    except:
        try:
            tree = etree.fromstring(path)
        except Exception:
            print(
                "Error: it was not able to read a path, a file-like object, or a string as an XML"
            )
            raise
    return tree


def stringify_children(node):
    """Joins all string parts excluding empty parts."""
    return "".join(text.strip() for text in node.itertext() if text)


def stringify_affiliation(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = (
        [node.text]
        + list(
            chain(
                *(
                    [c.text if (c.tag != "label" and c.tag != "sup") else "", c.tail]
                    for c in node.getchildren()
                )
            )
        )
        + [node.tail]
    )
    return " ".join(filter(None, parts))


def stringify_affiliation_rec(node):
    """
    Flatten and join list to string
    ref: http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    """
    parts = _recur_children(node)
    parts_flatten = list(_flatten(parts))
    return " ".join(parts_flatten).strip()


def _flatten(l):
    """
    Flatten list into one dimensional
    """
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, string_types):
            for sub in _flatten(el):
                yield sub
        else:
            yield el


def _recur_children(node):
    """
    Recursive through node to when it has multiple children
    """
    if len(node.getchildren()) == 0:
        parts = (
            ([node.text or ""] + [node.tail or ""])
            if (node.tag != "label" and node.tag != "sup")
            else ([node.tail or ""])
        )
        return parts
    else:
        parts = (
            [node.text or ""]
            + [_recur_children(c) for c in node.getchildren()]
            + [node.tail or ""]
        )
        return parts


def month_or_day_formater(month_or_day):
    """
    Parameters
    ----------
    month_or_day: str or int
        must be one of the following:
            (i)  month: a three letter month abbreviation, e.g., 'Jan'.
            (ii) day: an integer.

    Returns
    -------
    numeric: str
        a month of the form 'MM' or a day of the form 'DD'.
        Note: returns None if:
            (a) the input could not be mapped to a known month abbreviation OR
            (b) the input was not an integer (i.e., a day).
    """
    if month_or_day.replace(".", "") in filter(None, calendar.month_abbr):
        to_format = strptime(month_or_day.replace(".", ""), "%b").tm_mon
    elif month_or_day.strip().isdigit() and "." not in str(month_or_day):
        to_format = int(month_or_day.strip())
    else:
        return None

    return ("0" if to_format < 10 else "") + str(to_format)


def pretty_print(node):
    """
    Pretty print a given lxml node
    """
    print(etree.tostring(node, pretty_print=True).decode("utf-8"))
