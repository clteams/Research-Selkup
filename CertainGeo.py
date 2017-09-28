#!/usr/bin/python3
import json, sqlite3
dictionary = sqlite3.connect('dic.sqlite3')
dic = dictionary.cursor()
corpus = sqlite3.connect('corp.sqlite3')
corp = corpus.cursor()
new_corpus = sqlite3.connect('new-corp.sqlite3')
ncorp = new_corpus.cursor()

#CREATE TABLE srds_based_corpus(ind integer, selkup text, russian text, dialects text, links text);
try:
    ncorp.execute("create table srds_based_corpus(ind integer, selkup text, russian text, dialects text, links text)")
    ncorp.commit()
except:
    print('the table already exists')

all_rows = corp.execute("select ind, selkup, russian, dialects, links from srds_based_corpus").fetchall()
i = 0
for row in all_rows:
    # row [3] dialects
    if row[3] == '@':
        print('Row index {0}, geo = @, trying to detect CG/D'.format(i))
        words = dic.execute("select content from srds_dictionary where indx in ({0})".format(row[4])).fetchall()
        dialect = False
        for word in words:
            parsed = json.loads(word[0]) # word[0] is for `content`
            dialect = False
            for title in parsed['title']:
                if len(title['dialects']) == 1:
                    dialect = title['dialects'][0]
                    break
            if dialect:
                break
        row[3] = dialect if dialect else '@'
        ncorp.execute("insert into srds_based_corpus values(?, ?, ?, ?, ?)", row)
        print('DB insertion')
    else:
        print('Row index {0}, geo is not @, skip it!'.format(i))
    i += 1

new_corpus.commit()
corpus.commit()
dictionary.commit()
new_corpus.close()
corpus.close()
dictionary.close()
