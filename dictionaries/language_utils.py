#!/usr/bin/python3
# -*- coding: utf-8 -*
import codecs
import pymorphy2
__author__ = "gisly"

morph = pymorphy2.MorphAnalyzer()
YAT_WORDS = 'resources/yat_words.txt'
YAT = 'ѣ'
OUT_OF_VOC_WORDS = None
OUT_OF_VOC_WORDS_FILENAME = 'resources/out_of_voc_words.txt'

OLD_SPELLINGS = None
OLD_SPELLINGS_FILENAME = 'resources/old_spellings.txt'
OLD_SPELLING_DELIMITER = ':'

def check_pymorphy(word):
    cache_dictionaries()
    word_list = word.split(' ')
    for word_part in word_list:
        if not check_pymorphy_single(word_part):
            return False
    return True


def check_pymorphy_single(word):
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
