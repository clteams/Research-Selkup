#!/usr/bin/python3
import sqlite3
import csv
import io
import shutil
import datetime
import os
import re


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
        if self.ST != self.last_build:
            self.closest_path = self.closest_path + int(self.last_build[-1])
            self.ST = self.last_build

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
    def __init__(self):
        Master.__init__(self)
        self.D = '/.databases/'
        self.E = '/corpus.sqlite3'
        self.DE = '/dictionary.sqlite3'
        self.ST = self.today.strftime('%d-%m-%Y')
        self.src_db = self.D + self.closest_path + self.E
        self.src_dict = self.D + self.closest_path + self.DE
        self.dest_db = self.D + self.ST + self.E
        self.dest_dict = self.D + self.ST + self.DE
        assert not os.path.isabs(self.src_db)
        self.dest_dir = os.path.join(self.dest_db, os.path.dirname(self.src_db))
        self.dest_dict_dir = os.path.join(self.dest_dict, os.path.dirname(self.src_dict))
        os.makedirs(self.dest_dir)
        os.makedirs(self.dest_dict_dir)
        shutil.copy(self.src_db, self.dest_dir)
        shutil.copy(self.src_db, self.dest_dict_dir)
        self.db_loaded = sqlite3.connect(self.dest_db)
        self.db_cursor = self.db_loaded.cursor()
        self.max_crow_id = self.db_cursor.execute(
            'SELECT max(crow_id) FROM corpus'
        ).fetchone()[0]
        self.start_crow_id = int(self.max_crow_id) + 1

    def add_segment(self, **kwargs):
        for crow_function, crow_content in kwargs.items():
            if type(crow_content) != str:
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