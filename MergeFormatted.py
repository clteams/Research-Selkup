#!/usr/bin/python3
import re

class reg:
    w = r'[\wёқэ́ӓҗӣңёӧи́ӯӱ]'
    w_lex = w[:-1] + r'\s~]+'

fi = open('srds-formatted.txt').read()
o = 'srds-merged.txt'

stri = fi.splitlines()

with open(o, 'a') as out:
    continue_times = 0
    len_stri = len(stri)
    for i in range(len_stri):
        cs = stri[i]
        if continue_times > 0:
            continue_times -= 1
            continue
        j = i + 1
        if j == len_stri:
            continue
        while not re.search('^(\s\n|\s)*' + reg.w_lex + r'\/[^\/]+\/\s+[^«"]', stri[j]):
            print(j)
            cs += " " + stri[j]
            if j == len_stri - 1:
                break
            j += 1
            continue_times += 1
        out.write(re.sub(r'\s{2,}', ' ', cs) + "\n")
