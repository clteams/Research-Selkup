#!/usr/bin/python3
import re
import sqlite3

''' New SQLite DB scheme
create table dictionary(dict_id integer, dict_function text, dict_subid text, dict_content text); 
'''

dictionary = sqlite3.connect('./new_dictionary.sqlite3')
dict_agent = dictionary.cursor()

source_text = open('./dictionaries/resources/part1.txt_out.txt').read().splitlines()


class Value:
    def __init__(self, value, properties=None):
        self.value = value
        self.properties = properties if properties else []

    def add_props(self, properties):
        self.properties += properties

''' New SQLite DB scheme
create table dictionary(dict_id integer, dict_function text, dict_subid text, dict_content text); 
'''

index = 0
for line in source_text:
    russian, data = re.split(r'\s*=\s*', line)
    values = re.split(r'\s*,\s*', data)
    proper_values = []
    shady_values = []
    for value in values:
        value = value.strip()
        data = re.sub(r'\[([^\]]*)\](?!$)', '\g<1>', data)
        if '[' not in value:
            proper_values.append(value)
        else:
            try:
                comment = re.search(r'\[.*\]', value).group(0)[1:-1].strip()
                clear_value = re.sub(r'\s*\[.*\]', '', value)
                if re.search(r'зач[её]рк', comment):
                    shady_values.append(clear_value)
                elif re.search('исправл', comment):
                    mistake = re.sub(r'.*исправлено\s+из\s+', '', comment)
                    shady_values.append(mistake)
                    proper_values.append(clear_value)
            except AttributeError:
                pass
    GRIGOROVSKY_PATTERN = 'grigorovsky'
    CHA_PATTERN = 'CHA'
    for vals, status in ( (proper_values, 'proper'), (shady_values, 'shady') ):
        for val in vals:
            dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)', (index, 'dict.title', '@', val,)
            )
            dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)', (index, 'dict.value', '@', russian,)
            )
            dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)', (index, 'dict.dialect', '@', CHA_PATTERN,)
            )
            dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)', (index, 'dict.status', '@', status,)
            )
            dict_agent.execute(
                'insert into dictionary values (?, ?, ?, ?)', (index, 'dict.source', '@', GRIGOROVSKY_PATTERN,)
            )
            index += 1


dictionary.commit()
dictionary.close()