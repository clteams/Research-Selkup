#!/usr/bin/python3
import CorpusUpdate
import re
import string

my_db = CorpusUpdate.Database(update=True)

for j in (1, 2):

    extr_text = open('./resources/rasskazy-natashi/{}.txt'.format(j)).read().splitlines()
    
    for s in extr_text:
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
            prepare = {
                'text.selkup' : selkup_buffer,
                'lemmatized.selkup' : ['_' for _ in selkup_buffer],
                'text.russian' : russian_buffer,
                'metadata.source' : ['rasskazy_1_' + str(j)],
                'metadata.date' : ['10/12/2017'],
                'metadata.pushed_by' : ['admin']
            }
            if i != len(selkup_splitted) - 1:
                prepare['metadata.sequence'] = ['true']
            my_db.add_segment(prepare)

my_db.commit()
my_db.close()