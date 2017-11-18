#!/usr/bin/python
# -*- coding: utf-8 -*
__author__ = "gisly"
import lxml.html

def transform_to_html(data):
    return lxml.html.document_fromstring(data)

def get_children_by_parent_tag_attr(html, tag_name, attr_name, attr_value):
    return html.xpath('.//' + tag_name + '[@' + attr_name + '="' + attr_value + '"]/child::node()')


def get_first_html_tag(html,tag_name):
    results = html.xpath('.//'+tag_name)
    if results:
        return results[0]
    return None
