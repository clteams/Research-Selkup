#!/usr/bin/python3
import CorpusUpdate
import string

my_db = CorpusUpdate.Database()


selkup_text = open('./resources/chumel-calendar/calendar.txt', encoding='utf-8').read().splitlines()
russian_text = open('./resources/chumel-calendar/calendar-russian.txt', encoding='utf-8').read().splitlines()

for j, st in enumerate(selkup_text):
    selkup_splitted = [selkup_text[j]]
    russian_splitted = [russian_text[j]]

    for i, element in enumerate(selkup_splitted):
        tokenizer = CorpusUpdate.CorpusData(
            selkup=selkup_splitted[i],
            russian=russian_splitted[i]
        )
        tokenizer.extend_punct_list(['«', '»'])
        selkup_buffer, russian_buffer = tokenizer.tokenize_simple()

        prepare = {
            'text.selkup': selkup_buffer,
            'lemmatized.selkup': ['_' for _ in selkup_buffer],
            'text.russian': russian_buffer,
            'metadata.source': ['calendar'],
            'metadata.dialects': ['OB.CU'],
            'metadata.date': ['8/3/2018'],
            'metadata.pushed_by': ['admin']
        }
        if i != len(selkup_splitted) - 1:
            prepare['metadata.sequence'] = ['true']
        my_db.add_segment(prepare)

my_db.commit()
my_db.close()