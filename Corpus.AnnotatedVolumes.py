#!/usr/bin/python3

import sqlite3
import csv
import io
import re

corpus_database = sqlite3.connect('./corpus.sqlite3')
corpus = corpus_database.cursor()



corpus_database.commit()
corpus_database.close()