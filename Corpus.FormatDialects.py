#!/usr/bin/python3
import sqlite3
import csv
import io
import re

corpus_database = sqlite3.connect('./databases/29-09-2017-build/corpusget.sqlite3')
corpus = corpus_database.cursor()

prepare = 'SELECT crow_content from corpus where crow_function = "metadata.dialects"'
crow_metadata_dialects = corpus.execute(prepare).fetchall()
processed = {}

rx_ob_capital = r'[СШЧI]+'
rx_ob_capital_incl = rx_ob_capital[1:-2]


def get_csv(s):
    obj = csv.reader(s, quoting=csv.QUOTE_NONNUMERIC)
    obj = [x[0] for x in list(obj) if x != ['', ''] and x != []]
    return obj

for dialects_tuple in crow_metadata_dialects:
    src_dialects = dialects_tuple[0]
    dialects = get_csv(dialects_tuple[0])[0]
    if dialects == '':
        continue
    if src_dialects in processed:
        continue
    replacement = []
    if 'об' in dialects and not re.search(rx_ob_capital, dialects):
        replacement.append('OB.COMMON')
    elif 'об' in dialects:
        for dlc in re.findall(rx_ob_capital, dialects):
            if dlc == 'С':
                replacement.append("OB.SU")
            elif dlc == 'Ч':
                replacement.append("OB.CU")
            elif dlc == 'Ш':
                replacement.append("OB.SO")
            elif 'I' in dlc:
                replacement.append("OB.SO")
        dialects = re.sub(r'об\.?[,\.\s' + rx_ob_capital_incl + ']+', '', dialects)

    dialect_codes = (
        ('ел', 'EL'),
        ('кет', 'KET'),
        ('вас', 'VAS'),
        ('тур', 'TUR'),
        ('тым', 'TYM')
    )
    for dlct_pair in dialect_codes:
        if dlct_pair[0] in dialects:
            replacement.append(dlct_pair[1])

    processed[src_dialects] = replacement

for dialect_wr in processed:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(processed[dialect_wr])
    prepare = "UPDATE corpus SET crow_content = ? where crow_function = ? and crow_content = ?"
    corpus.execute(prepare, (output.getvalue(), 'metadata.dialects', dialect_wr,))



corpus_database.commit()
corpus_database.close()