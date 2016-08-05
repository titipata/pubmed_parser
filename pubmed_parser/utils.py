import collections
from six import string_types
from lxml import etree
from itertools import chain


def read_xml(path):
    """
    Parse tree from given XML path
    """
    try:
        tree = etree.parse(path)
    except:
        try:
            tree = etree.fromstring(path)
        except Exception as e:
            print("Error: it was not able to read a path, a file-like object, or a string as an XML")
            raise
    return tree


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


def stringify_affiliation_rec(node):
    """
    Flatten and join list to string
    ref: http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    """
    parts = _recur_children(node)
    parts_flatten = list(_flatten(parts))
    return ' '.join(parts_flatten).strip()


def _flatten(l):
    """
    Flatten list into one dimensional
    """
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, string_types):
            for sub in _flatten(el):
                yield sub
        else:
            yield el


def _recur_children(node):
    """
    Recursive through node to when it has multiple children
    """
    if len(node.getchildren()) == 0:
        parts = ([node.text or ''] + [node.tail or '']) if (node.tag != 'label' and node.tag !='sup') else ([node.tail or ''])
        return parts
    else:
        parts = ([node.text or ''] +
                 [_recur_children(c) for c in node.getchildren()] +
                 [node.tail or ''])
        return parts
