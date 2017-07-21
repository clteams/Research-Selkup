#!/usr/bin/python3
import json
import sqlite3
import selkup_alphabet
import re

class processing:
    def __init__(self, string):
        self.string = string
        self.basic_rep()
        self.srds_rep()
        self.yk_rep()
    def basic_rep(self):
        self.string = selkup_alphabet.uni.unify(self.string, strict_only = True)
    def yk_rep(self):
        repl_map = [            
            [r'([ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)$', '\g<1>й'],
            [r'([^ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)$', '\g<1>и̇'],
            [r'([ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)\s', '\g<1>й '],
            [r'([^ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)\s', '\g<1>и̇ '],
            [r'([^ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)([^ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])', '\g<1>и̇\g<3>'],
            [r'([ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)([ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])', '\g<1>й\g<3>'],
            [r'([ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)([^ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])', '\g<1>й\g<3>'],
            [r'([^ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])(й|и́)([ё̄е̄ы̄ӧӧ̄о̄ю̈ю̈̄ю̄я̄ӭӭ̄э̄ӓӓ̄āӱ̄ӯёеоюуяаэиы])', '\g<1>и̇\g<3>']               
        ]
        for pair in repl_map:
            from_ = self.string
            self.string = re.sub(pair[0], pair[1], self.string)
            if from_ != self.string:
                break
    def srds_rep(self):
        repl_map = [
            ["о́", "ӧ"],
            ["э́", "ӭ"],
            ["у́", "ӱ"],
            ["а́", "ӓ"],
            ["ю́", "ю̈"],
            ["О́", "Ӧ"],
            ["Э́", "Ӭ"],
            ["У́", "Ӱ"],
            ["А́", "Ӓ"],
            ["Ю́", "Ю̈"],
        ]
        for pair in repl_map:
            self.string = self.string.replace(pair[0], pair[1])
    def get_string(self):
        return self.string

dictionary = sqlite3.connect('dic.sqlite3')
dic = dictionary.cursor()

new_dictionary = sqlite3.connect('new-dic.sqlite3')
ndic = new_dictionary.cursor()

corpus = sqlite3.connect('corp.sqlite3')
corp = corpus.cursor()

new_corpus = sqlite3.connect('new-corp.sqlite3')
ncorp = new_corpus.cursor()

try:
    ndic.execute('create table srds_dictionary(indx int, title text, content text)')
except:
    pass

try:
    ncorp.execute (
        'create table srds_based_corpus(ind integer, selkup text, russian text, dialects text, links text)'
    )
except:
    pass

#CREATE TABLE srds_dictionary(indx int, title text, content text);

dic_rows = dic.execute('select indx, title, content from srds_dictionary').fetchall()
dic_rows_length = len(dic_rows)

row_index = 0
commit_interval = 300
start_from = -1

for row in dic_rows:
    print('|||')
    indx = int(row[0])
    if indx < start_from:
        continue
    print('Reading row {0} from old database...'.format(indx))
    title = processing(row[1]).get_string()
    #content = str(json.loads(row[2]))
    #content = processing(content).get_string()
    #content = json.dumps(eval(content))
    content = row[2]
    print('Writing to new database...')
    ndic.execute('insert into srds_dictionary values(?, ?, ?)', (indx, title, content,))
    row_index += 1
    if not indx % commit_interval:
        new_dictionary.commit()
        print('-- Committing --')
new_dictionary.commit()
print('-- Committing --')
print('Switching to corpus!')
#CREATE TABLE srds_based_corpus(ind integer, selkup text, russian text, dialects text, links text);
corp_rows = corp.execute('select ind, selkup, russian, dialects, links from srds_based_corpus').fetchall()
for row in corp_rows:
    print('Reading row {0} from old database...'.format(indx))
    ind = int(row[0])
    selkup = row[1]
    russian = row[2]
    dialects = row[3]
    links = row[4]
    selkup = processing(selkup).get_string()
    print('Writing to new database...')
    ncorp.execute (
        'insert into srds_based_corpus values(?,?,?,?,?)',
        (ind, selkup, russian, dialects, links,)
    )
    if not ind % commit_interval:
        new_corpus.commit()
        print('-- Committing --')
new_corpus.commit()
new_dictionary.commit()
new_dictionary.close()
dictionary.close()
new_corpus.close()
corpus.close()
