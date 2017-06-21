#!/usr/bin/python3
import json
import sqlite3

dictionary = sqlite3.connect('dic.sqlite3')
dic = dictionary.cursor()

new_dictionary = sqlite3.connect('20-dic.sqlite3')
ndic = new_dictionary.cursor()
ndic.execute('create table srds_dictionary(ind int, title text, content text)')

#CREATE TABLE srds_dictionary(indx int, title text, content text);

all = c.execute('select indx, title, content from srds_dictionary').fetchall()

rep = [
    []
]

new_dictionary.close()
dictionary.close()
