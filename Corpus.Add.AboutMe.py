#!/usr/bin/python3
import CorpusUpdate
import re
import string

my_db = CorpusUpdate.Database()

about_me = open('./resources/about-me.txt').read().splitlines()

for s in about_me:
    s = re.sub(r'^\d+\.\s*', '', s)
    if s == '':
        continue

    selkup, russian = re.split('\s*–\s*(?=[А-Я])', s, 1)
    selkup_splitted = [x for x in re.split(r'\s*[\.!\?]\s*', selkup) if x != '']
    russian_splitted = [x for x in re.split(r'\s*[\.!\?]\s*', russian) if x != '']

    punct = [x for x in string.punctuation]
    punct += ['«', '»']
    punct_before = False
    for i in range(len(selkup_splitted)):
        selkup_buffer = [""]
        for s in selkup_splitted[i]:
            if s == " ":
                selkup_buffer.append("")
            elif s in punct:
                selkup_buffer.append(s)
                punct_before = True
            else:
                if punct_before:
                    selkup_buffer.append("")
                    punct_before = False
                selkup_buffer[-1] += s
        selkup_buffer = [x for x in selkup_buffer if x != '']
        russian_buffer = [""]
        for s in russian_splitted[i]:
            if s == " ":
                russian_buffer.append("")
            elif s in punct:
                russian_buffer.append(s)
                punct_before = True
            else:
                if punct_before:
                    russian_buffer.append("")
                    punct_before = False
                russian_buffer[-1] += s
        my_db.add_segment({
            'text.selkup' : selkup_buffer,
            'lemmatized.selkup' : ['_' for _ in range(len(selkup_buffer))],
            'text.russian' : russian_buffer,
            'metadata.source' : 'pro_sebya',
            'metadata.date' : '10/11/2017',
            'metadata.pushed_by' : 'admin',
            'metadata.sequence' : 'true'
        })

my_db.commit()
my_db.close()