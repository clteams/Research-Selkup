#!/usr/bin/python3
import sqlite3
import csv
import io
import shutil
import datetime
import os
import re
import string


class Master:
    def __init__(self):
        self.all_dbs = os.listdir('./databases')
        self.dts = []
        for db_catalogue in self.all_dbs:
            if '.' in db_catalogue:
                continue

            int_date = re.findall(r'\d+(?=-)', db_catalogue)
            int_date.reverse()
            int_date = [int(x) for x in int_date]
            self.dts.append(datetime.datetime(*int_date))

        self.today = datetime.datetime.now()
        self.closest = min(self.dts, key=lambda x: abs(x - self.today))
        self.closest_path = self.closest.strftime('%d-%m-%Y') + '-build'
        self.closest_path = self.get_last_build(self.closest_path, self.all_dbs)
        self.ST = self.today.strftime('%d-%m-%Y') + '-build'
        self.last_build = self.get_last_build(self.ST, self.all_dbs)
        if self.last_build != False:
            try:
                index_decr = int(self.last_build[-1]) - 1
                if index_decr > 2:
                    self.closest_path += str(index_decr)
                self.ST = self.last_build[:-1] + str(int(self.last_build[-1]) + 1)
            except ValueError:
                self.ST += '2'

    @staticmethod
    def get_last_build(path, parent):
        max_index = 0
        at_least_one = False
        for catalogue in parent:
            if not catalogue.startswith(path):
                continue
            at_least_one = True
            index = re.findall(r'\d+$', catalogue)
            index = 0 if len(index) == 0 else int(index[0])
            if index > max_index:
                max_index = index
        if max_index > 0:
            path += str(max_index)
        return path if at_least_one else False


class Database(Master):
    def __init__(self, update=False):
        Master.__init__(self)
        self.D = './databases/'
        self.E = '/corpus.sqlite3'
        self.DE = '/dictionary.sqlite3'
        self.src_db = self.D + self.closest_path + self.E
        self.src_dict = self.D + self.closest_path + self.DE
        self.dest_db = self.D + self.ST + self.E
        self.dest_dict = self.D + self.ST + self.DE

        if not update:
            try:
                assert not os.path.isabs(self.src_db)
            except AssertionError:
                print('assertion does not work')
            self.dest_dir = self.D + self.ST
            os.makedirs(self.dest_dir)
            shutil.copy(self.src_db, self.dest_dir)
            shutil.copy(self.src_dict, self.dest_dir)
            self.db_loaded = sqlite3.connect(self.dest_db)
        else:
            self.db_loaded = sqlite3.connect(self.src_db)

        self.db_cursor = self.db_loaded.cursor()
        self.max_crow_id = self.db_cursor.execute(
            'SELECT max(crow_id) FROM corpus'
        ).fetchone()[0]
        self.start_crow_id = int(self.max_crow_id) + 1

    def add_segment(self, kwargs):
        for crow_function, crow_content in kwargs.items():
            output = io.StringIO()
            writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(crow_content)
            crow_content = output.getvalue()
            self.db_cursor.execute('INSERT INTO corpus VALUES (?, ?, ?)',
                (self.start_crow_id, crow_function, crow_content,)
            )
        self.start_crow_id += 1

    def commit(self):
        self.db_loaded.commit()

    def close(self):
        self.db_loaded.close()


class CorpusData:
    def __init__(self, **kwargs):
        self.data = kwargs
        self.punct_list = [x for x in string.punctuation if x != '~']

    def extend_punct_list(self, ext_list):
        self.punct_list += ext_list

    def tokenize_simple(self):
        crow_text = dict()
        crow_text['selkup'] = ['']
        crow_text['russian'] = ['']
        self.data['selkup'] = re.sub(r'\s*\([^\)]*\)', '', self.data['selkup'])
        self.data['russian'] = re.sub(r'\s*\([^\)]*\)', '', self.data['russian'])
        last_index = dict()
        last_index['selkup'] = len(self.data['selkup']) - 1
        last_index['russian'] = len(self.data['russian']) - 1\

        for lang in ('selkup', 'russian'):
            for e, sym in enumerate(self.data[lang]):
                if sym != ' ' and sym not in self.punct_list:
                    crow_text[lang][-1] += sym
                elif sym == ' ':
                    crow_text[lang].append('')
                elif sym not in ('-', '–'):
                    crow_text[lang].append(sym)
                    crow_text[lang].append('')
                else:
                    if e == 0 or e == last_index[lang] or self.data[lang][e - 1] == ' ' \
                            or self.data[lang][e + 1] == ' ':
                        crow_text[lang].append(sym)
                        crow_text[lang].append('')
                    else:
                        crow_text[lang][-1] += sym

        crow_text['selkup'] = [x for x in crow_text['selkup'] if x != '']
        crow_text['russian'] = [x for x in crow_text['russian'] if x != '']

        return crow_text['selkup'], crow_text['russian']
