#!/usr/bin/python3
import CorpusUpdate
import string

my_db = CorpusUpdate.Database(update=True)

for a in (1, 2):

    selkup_text = open('./resources/izhenbina_AT/{}.txt'.format(a)).read().splitlines()
    russian_text = open('./resources/izhenbina_AT/{}-russian.txt'.format(a)).read().splitlines()

    for j in range(len(selkup_text)):
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
                'metadata.source': ['izhenbinaAT_' + str(a)],
                'metadata.date': ['10/12/2017'],
                'metadata.pushed_by': ['admin']
            }
            if i != len(selkup_splitted) - 1:
                prepare['metadata.sequence'] = ['true']
            my_db.add_segment(prepare)

my_db.commit()
my_db.close()