#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------------------------------------------------------------
# includes

# 2+3 compat
from __future__ import absolute_import, division, print_function, unicode_literals

# standards
import re

# 3rd parties
import pytest

# klon
from klon import Klon
from klon.lxml import LxmlKlon

#----------------------------------------------------------------------------------------------------------------------------------

def parametrize_implementations(body):
    parametrize = pytest.mark.parametrize('klon', [Klon, LxmlKlon])
    return parametrize(body)


def check(element, tag, attrib={}, children=[], text=None, tail=None):
    assert element.tag == tag
    assert element.attrib == attrib
    assert element.text == text
    assert len(element) == len(children)
    for child, child_definition in zip(element, children):
        check(child, **child_definition)
    assert element.tail == tail


def check_str(klon, element, expected_str):
    generated_bytes = klon.tostring(element, encoding='UTF-8')
    generated_str = generated_bytes.decode('UTF-8')
    assert _normalise_str(generated_str) == _normalise_str(expected_str)

def _normalise_str(text):
    # Smoothe over the slight cosmetic differences btw the output of xml.etree.ElementTree.tostring and lxml.etree.tostring
    text = re.sub(r'^<\?xml[^>]*>\s*', '', text)
    text = re.sub(r' (?=/>)', '', text)
    return text

#----------------------------------------------------------------------------------------------------------------------------------

@parametrize_implementations
def test_build_empty_node(klon):
    element = klon.build_etree('mynode')
    check(element, 'mynode')
    check_str(klon, element, '<mynode />')


@parametrize_implementations
def test_build_attrib_from_dict(klon):
    element = klon.build_etree('mynode', {'a': '1'})
    check(element, 'mynode', {'a': '1'})
    check_str(klon, element, '<mynode a="1" />')

#----------------------------------------------------------------------------------------------------------------------------------

@parametrize_implementations
def test_css_style_id(klon):
    element = klon.build_etree('mynode#test')
    check(element, 'mynode', {'id': 'test'})
    check_str(klon, element, '<mynode id="test" />')


@parametrize_implementations
def test_css_style_class(klon):
    element = klon.build_etree('mynode.test')
    check(element, 'mynode', {'class': 'test'})
    check_str(klon, element, '<mynode class="test" />')

#----------------------------------------------------------------------------------------------------------------------------------

@parametrize_implementations
def test_build_node_with_text(klon):
    element = klon.build_etree('mynode', 'Text')
    check(element, 'mynode', text='Text')
    check_str(klon, element, '<mynode>Text</mynode>')


@parametrize_implementations
def test_build_node_with_multiple_text(klon):
    element = klon.build_etree('mynode', 'Te', 'xt')
    check(element, 'mynode', text='Text')
    check_str(klon, element, '<mynode>Text</mynode>')


@parametrize_implementations
def test_build_node_with_text_and_attrib(klon):
    element = klon.build_etree('mynode', {'a': '1'}, 'Te', 'xt')
    check(element, 'mynode', attrib={'a': '1'}, text='Text')
    check_str(klon, element, '<mynode a="1">Text</mynode>')

#----------------------------------------------------------------------------------------------------------------------------------

@parametrize_implementations
def test_node_with_children(klon):
    element = klon.build_etree('mynode', ['mychild'])
    check(element, 'mynode', children=[{'tag': 'mychild'}])
    check_str(klon, element, '<mynode><mychild /></mynode>')


@parametrize_implementations
def test_node_with_children_attribs(klon):
    element = klon.build_etree('mynode', ['mychild', {'a': '1'}])
    check(element, 'mynode', children=[{'tag': 'mychild', 'attrib': {'a': '1'}}])
    check_str(klon, element, '<mynode><mychild a="1" /></mynode>')


@parametrize_implementations
def test_node_with_children_text(klon):
    element = klon.build_etree('mynode', ['mychild', {'a': '1'}, 'Text'])
    check(element, 'mynode', children=[{'tag': 'mychild', 'attrib': {'a': '1'}, 'text': 'Text'}])
    check_str(klon, element, '<mynode><mychild a="1">Text</mychild></mynode>')


@parametrize_implementations
def test_node_with_children_tail(klon):
    element = klon.build_etree('mynode', ['mychild'], 'Tail')
    check(element, 'mynode', children=[{'tag': 'mychild', 'tail': 'Tail'}])
    check_str(klon, element, '<mynode><mychild />Tail</mynode>')


@parametrize_implementations
def test_node_with_prebuilt_child(klon):
    child = klon.build_etree('mychild')
    element = klon.build_etree('mynode', child)
    check(element, 'mynode', children=[{'tag': 'mychild'}])
    check_str(klon, element, '<mynode><mychild /></mynode>')

#----------------------------------------------------------------------------------------------------------------------------------

@parametrize_implementations
def test_non_str_tag(klon):
    with pytest.raises(ValueError):
        klon.build_etree(object(), {'a': '1'})

@parametrize_implementations
def test_byte_tag(klon):
    with pytest.raises(ValueError):
        klon.build_etree(b'mytag', {'a': '1'})

@parametrize_implementations
def test_empty_children_array_are_noop(klon):
    element = klon.build_etree('mynode', ['mychild', 'a', [], 'b'], [], 'c')
    check(element, 'mynode', children=[{'tag': 'mychild', 'text': 'ab', 'tail': 'c'}])
    check_str(klon, element, '<mynode><mychild>ab</mychild>c</mynode>')

@parametrize_implementations
def test_none_values_are_noop(klon):
    element = klon.build_etree('mynode', ['mychild', 'a', None, 'b'], None, 'c')
    check(element, 'mynode', children=[{'tag': 'mychild', 'text': 'ab', 'tail': 'c'}])
    check_str(klon, element, '<mynode><mychild>ab</mychild>c</mynode>')

#----------------------------------------------------------------------------------------------------------------------------------
