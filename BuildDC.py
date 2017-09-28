#!/usr/bin/python3
import json
import sqlite3

sym_rep = {
    'гх': 'ӷ',
    'дф': '?',
    'ю̈' : 'ӱ',
    'ҙ' : 'дз',
    'қ' : 'ӄ',
    'ң' : 'ӈ',
    'ӌ' : 'ч',
    'ҷ' : 'ч',
    'дж' : 'җ'
}

inp = json.loads(open('srds-parsed.json').read())['SRDS']

i = 0
corp_i = 0

dictionary = sqlite3.connect('dic.sqlite3')
dic = dictionary.cursor()

corpus = sqlite3.connect('corp.sqlite3')
cor = corpus.cursor()

for article in inp:
    print('dic', i)
    if i % 150 == 0:
        dictionary.commit()
        corpus.commit()
    art = str(article)
    for sr in sym_rep:
        art = art.replace(sr, sym_rep[sr])
    art = eval(art)
    indices = []
    for title in art['title']:
        dic.execute('insert into srds_dictionary values (?, ?, ?)', (i, title['query'], json.dumps(article),))
        indices.append(str(i))
        i += 1
    indices_joined = ','.join(indices)
    for p in art['lexic']:
        if 'examples' in p:
            if len(p['examples']) > 0:
                print('corp', corp_i)
                for ex in p['examples']:
                    selkup = ex['selkup']
                    if 'russian' in ex:
                        russian = ex['russian']
                    else:
                        russian = '@'
                    if 'dialects' in ex:
                        dialects = '|'.join(ex['dialects'])
                    else:
                        dialects = '@'
                    cor.execute(
                        'insert into srds_based_corpus values(?, ?, ?, ?, ?)',
                        (corp_i, selkup, russian, dialects, indices_joined,)
                    )
                    corp_i += 1
dictionary.commit()
corpus.commit()
dictionary.close()
corpus.close()
