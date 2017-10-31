#!/usr/bin/python3
import CorpusUpdate
import re
import string

my_db = CorpusUpdate.Database(update=True)

about_me = open('./resources/about-me.txt').read().splitlines()

for s in about_me:
    s = re.sub(r'^\d+\.\s*', '', s)
    if s == '':
        continue

    selkup, russian = re.split('\s*–\s*(?=[А-Я])', s, 1)
    selkup_splitted = [x for x in re.split(r'\s*[\.!\?]\s*', selkup) if x != '']
    russian_splitted = [x for x in re.split(r'\s*[\.!\?]\s*', russian) if x != '']

    for e, element in enumerate(selkup_splitted):
        tokenizer = CorpusUpdate.CorpusData(
            selkup=selkup_splitted[e],
            russian=russian_splitted[e]
        )
        tokenizer.extend_punct_list(['«', '»'])
        selkup_buffer, russian_buffer = tokenizer.tokenize_simple()
        my_db.add_segment({
            'text.selkup' : selkup_buffer,
            'lemmatized.selkup' : ['_' for _ in selkup_buffer],
            'text.russian' : russian_buffer,
            'metadata.source' : ['pro_sebya'],
            'metadata.date' : ['10/11/2017'],
            'metadata.pushed_by' : ['admin'],
            'metadata.sequence' : ['true']
        })

my_db.commit()
my_db.close()