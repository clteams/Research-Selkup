#!/usr/bin/python3
import CorpusUpdate
import re
import string

my_db = CorpusUpdate.Database()

for a in (1, 2):

    selkup_text = open('./resources/izhenbina_AT/{}.txt'.format(a)).read().splitlines()
    russian_text = open('./resources/izhenbina_AT/{}-russian.txt'.format(a)).read().splitlines()

    for j in range(len(selkup_text)):
        selkup_splitted = [selkup_text[j]]
        russian_splitted = [russian_text[j]]

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
            prepare = {
                'text.selkup': selkup_buffer,
                'lemmatized.selkup': ['_' for _ in range(len(selkup_buffer))],
                'text.russian': russian_buffer,
                'metadata.source': ['izhenbinaAT_' + str(a)],
                'metadata.date': ['10/12/2017'],
                'metadata.pushed_by': ['admin']
            }
            if i != len(selkup_splitted) - 1:
                prepare['metadata.sequence'] = ['true']
            my_db.add_segment(prepare)

my_db.commit()
my_db.close()