#!/usr/bin/python3

import sqlite3
import csv
import io
import string
from difflib import SequenceMatcher

'''
    New Database Schema
        CREATE TABLE corpus(crow_id integer, crow_function text, crow_content text)

    Old (SRDS) Database Schema
        CREATE TABLE srds_based_corpus(ind integer, selkup text, russian text, dialects text, links text)
'''

corpus_database = sqlite3.connect('./databases/25-07-2017-build/corpus.sqlite3')
dictionary_database = sqlite3.connect('./databases/25-07-2017-build/dictionary.sqlite3')
new_corpus_database = sqlite3.connect('new_corpus.sqlite3')

corpus_db = corpus_database.cursor()
dictionary_db = dictionary_database.cursor()
new_corpus_db = new_corpus_database.cursor()

old_corpus = corpus_db.execute("SELECT * FROM srds_based_corpus").fetchall()


class Indices:
    ind = 0
    selkup = 1
    russian = 2
    dialects = 3
    links = 4

crow_id = 0

for row in old_corpus:
    if row[Indices.russian] == '@':
        continue

    links = "(" + row[Indices.links] + ")"
    prepare = 'SELECT title from srds_dictionary where indx in ' + links
    link_words = [x for x in dictionary_db.execute(prepare).fetchall()]

    punct_list = [x for x in string.punctuation]

    crow_selkup_text = ['']
    crow_russian_text = ['']

    for sym in row[Indices.selkup]:
        if sym != ' ' and sym not in punct_list:
            crow_selkup_text[len(crow_selkup_text) - 1] += sym
        elif sym == ' ':
            crow_selkup_text.append('')
        else:
            crow_selkup_text.append(sym)
            crow_selkup_text.append('')

    for sym in row[Indices.russian]:
        if sym != ' ' and sym not in punct_list:
            crow_russian_text[len(crow_russian_text) - 1] += sym
        elif sym == ' ':
            crow_russian_text.append('')
        else:
            crow_russian_text.append(sym)
            crow_russian_text.append('')

    class ExtractLemma:
        def __init__(self, l_words):
            self.link_words = l_words
            self.results = {}

        def check(self, token):
            matching_int = []
            matching_str = []
            for word in self.link_words:
                matching_int.append(SequenceMatcher(None, word, token).ratio())
                matching_str.append(word)
            m = max(matching_int)
            max_index = [a for a, b in enumerate(matching_int) if b == m][0]
            self.results[max_index] = (token, matching_str[max_index])

        def extract(self):
            relevant = max(list(self.results))
            return relevant, self.results[relevant][0], self.results[relevant][1]


    crow_selkup_lemmatized = []

    if '~' in crow_selkup_text:
        for token in crow_selkup_text:
            if token != '~':
                crow_selkup_lemmatized.append('')
            else:
                crow_selkup_lemmatized.append(link_words[0])
    else:
        extractor = ExtractLemma(link_words)
        for token in crow_selkup_text:
            extractor.check(token)
        rel = extractor.extract()
        for token in crow_selkup_text:
            if token != rel[1]:
                crow_selkup_lemmatized.append('')
            else:
                crow_selkup_lemmatized.append(rel[2])

    for data, func in (
        (crow_selkup_text, 'text.selkup'),
        (crow_selkup_lemmatized, 'lemmatized.selkup'),
        (crow_russian_text, 'text.russian')
    ):
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(data)
        prepare = "INSERT INTO corpus VALUES (?, ?, ?)"
        new_corpus_database.execute(prepare, (crow_id, func, output.getvalue(),))

    crow_id += 1
    print(crow_id)

corpus_database.commit()
dictionary_database.commit()
new_corpus_database.commit()

corpus_database.close()
dictionary_database.close()
new_corpus_database.close()