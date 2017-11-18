#!/usr/bin/python3
# -*- coding: utf-8 -*
import codecs
import pymorphy2
import web_utils
import html_utils
import dictionary_utils

__author__ = "gisly"

morph = pymorphy2.MorphAnalyzer()
YAT_WORDS = 'resources/yat_words.txt'
YAT = 'ѣ'
OUT_OF_VOC_WORDS = None
OUT_OF_VOC_WORDS_FILENAME = 'resources/out_of_voc_words.txt'

OLD_SPELLINGS = None
OLD_SPELLINGS_FILENAME = 'resources/old_spellings.txt'
OLD_SPELLING_DELIMITER = ':'

SELKUP_SITE_URL = 'http://selkup.org/dict-search'

SUFFIX_LIST = ['-ка', '-то']
PREFIX_LIST = ['по-']

TYPICAL_LENGTH = 20

def check_pymorphy(word):
    cache_dictionaries()
    word_list = word.split(' ')
    for word_part in word_list:
        if not check_pymorphy_single(word_part):
            return False
    return True

def check_selkup_word(word, translation):
    CHECK_FUNCTIONS = [check_pos]

    for check_function in CHECK_FUNCTIONS:
        if not check_function(word, translation):
            return False
    return True

def check_dictionary(word, translation):
    rus_translation_str = ' '.join(translation)
    #selkup_from_dict_list = get_selkup_from_dictionary(rus_translation_str)
    selkup_from_dict_list = dictionary_utils.get_selkup_by_meaning(rus_translation_str)
    for selkup_from_dict in selkup_from_dict_list:
        if is_similar(word, selkup_from_dict):
            return True
        print(word, selkup_from_dict)
    return False

def check_pos(word, translation):
    return True

def check_length(word, translation):
    return len(word) <= TYPICAL_LENGTH



def get_selkup_from_dictionary(translation):
    data = web_utils.get_url_data(SELKUP_SITE_URL, 'utf-8', {'word': translation,
                                                             'lemma': '1',
                                                             'lang': 'ru', })

    html_data = html_utils.transform_to_html(data)
    search_result = html_utils.get_first_html_tag(html_data, 'ol')
    res = []
    for element in search_result:
        children = element.xpath('child::node()')
        if children and not 'не найдено' in children[0]:
            res.append(children[0].text)
    return res


def is_similar(word1, word2):
    #TODO
    return word1.strip().lower() == word2.strip().lower()

def check_pymorphy_single(word):
    word = word.replace('́', '')
    if check_pymorphy_dict(word):
        return True
    for suffix in SUFFIX_LIST:
        if word.endswith(suffix) and check_pymorphy_dict(word[0:-len(suffix)]):
            return True

    for prefix in PREFIX_LIST:
        if word.startswith(prefix) and check_pymorphy_dict(word[len(prefix):]):
            return True
    return False


def check_pymorphy_dict(word):
    if word.lower() in OUT_OF_VOC_WORDS:
        return True
    return morph.parse(word)[0].is_known


def change_old_spellings(word):
    for old_spelling in OLD_SPELLINGS.items():
        word = word.replace(old_spelling[0], old_spelling[1])
    return word

def cache_dictionaries():
    cache_out_of_voc_words()
    cache_old_spellings()

def cache_out_of_voc_words():
    global OUT_OF_VOC_WORDS
    if OUT_OF_VOC_WORDS is None:
        OUT_OF_VOC_WORDS = set()
        with codecs.open(OUT_OF_VOC_WORDS_FILENAME, 'r', 'utf-8') as fin:
            for line in fin:
                OUT_OF_VOC_WORDS.add(line.strip().lower())


def cache_old_spellings():
    global OLD_SPELLINGS
    if OLD_SPELLINGS is None:
        OLD_SPELLINGS = dict()
        with codecs.open(OLD_SPELLINGS_FILENAME, 'r', 'utf-8') as fin:
            for line in fin:
                parts = line.strip().lower().split(OLD_SPELLING_DELIMITER)
                OLD_SPELLINGS[parts[0]] = parts[1]

