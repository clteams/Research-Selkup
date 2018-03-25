#!/usr/bin/python3

import re
import is_russian

selk = open('../resources/slsrrs/slsrrs_selkup.txt', encoding='utf-8').read()
selk = selk.splitlines()
checker = is_russian.Checker(import_op=False)
dict_result = {}


for line in selk:
    splitted_line = [[]]
    for token in line.split():
        if re.search('\d[\)\.]|—', token):
            splitted_line[-1].append(token)
            continue
        if not checker.check(token) and len(splitted_line) >= 1 and splitted_line[-1]:
            splitted_line.append([])
        splitted_line[-1].append(token)
    segment_title = []
    segment_translation = []
    start_russian = False
    for segment in splitted_line:
        if start_russian:
            dict_result[' '.join(segment_title)] = ' '.join(segment_translation)
            segment_title = []
            segment_translation = []
            start_russian = False

        segment_title.append(segment[0])
        i = 1
        while i < len(segment) and not checker.check(segment[i]):
            segment_title.append(segment[i])
            i += 1
        if i < len(segment):
            start_russian = True
            while i < len(segment):
                segment_translation.append(segment[i])
                i += 1

    print(dict_result)