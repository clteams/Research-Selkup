#!/usr/bin/python3
import json
import sqlite3
import selkup_alphabet

dictionary = sqlite3.connect('dic.sqlite3')
dic = dictionary.cursor()

new_dictionary = sqlite3.connect('new-dic.sqlite3')
ndic = new_dictionary.cursor()

corpus = sqlite3.connect('corp.sqlite3')
corp = corpus.cursor()

new_corpus = sqlite3.connect('new-corp.sqlite3')
ncorp = new_corpus.cursor()

try:
    ndic.execute('create table srds_dictionary(ind int, title text, content text)')
except:
    pass


#CREATE TABLE srds_dictionary(indx int, title text, content text);

dic_rows = dic.execute('select indx, title, content from srds_dictionary').fetchall()
dic_rows_length = len(dic_rows)
row_index = 0
commit_interval = 300
for row in dic_rows:
    indx = int(row[0])
    print('Reading row {0} from old database...'.format(indx))
    title = selkup_alphabet.unify(row[1], strict_only = True)
    content = str(json.loads(row[2]))
    content = selkup_alphabet.unify(content, strict_only = True)
    content = json.dumps(eval(content))
    print('Writing to new database...')
    ndic.execute('insert into table srds_dictionary values(?, ?, ?)', (indx, title, content,))
    row_index += 1
    if not indx % commit_interval:
        ndic.commit()
        print('-- Committing --')
#CREATE TABLE srds_based_corpus(ind integer, selkup text, russian text, dialects text, links text);
corp_rows = corp.execute('select ind, selkup, russian, dialects, links from srds_based_corpus').fetchall()
for row in corp_rows:
    ind = int(row[0])
    selkup = row[1]
    russian = row[2]
    dialects = row[3]
    links = row[4]
    selkup = selkup_alphabet.unify(selkup, strict_only = False)
    ncorp.execute (
        'insert into table srds_based_corpus values(?,?,?,?,?)',
        (ind, selkup, russian, dialects, links,)
    )
    if not ind % commit_interval:
        ncorp.commit()
        print('-- Committing --')
new_dictionary.close()
dictionary.close()
new_corpus.close()
corpus.close()
