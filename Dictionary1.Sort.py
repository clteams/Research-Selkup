#!/usr/bin/python3
import re


def clear_diacr(l):
    l = l.replace('̅', '')
    repl = {
        "ё̄": "ё",
        "ӧ̄": "ӧ",
        "ю̈̄": "ю̈",
        "ӭ̄": "ӭ",
        "ӓ̄": "ӓ",
        "ӱ̄": "ӱ",
        "и̇̄": "ӣ",
        "е̄": "е",
        "о̄": "о",
        "ю̄": "ю",
        "я̄": "я",
        "э̄": "э",
        "ā": "а",
        "ӯ": "у",
        "ӣ": "и",
        "ӄ": "к",
        "ӷ": "г",
        "ӈ": "н",
        "җ": "ж",
        "á": "а",
        "ō": "о",
        "ó": "о",
        "ý": "у",
        "ҷ": "ч"
    }
    l = l.replace("́", "")
    for key in repl:
        l = l.replace(key, repl[key])
    return l.lower()


alph = 'аӓбвгӷдеёжҗзии̇йкӄлмнӈоӧпрстуӱфхцчҷшщъыьэюя'
dictionary = open('Dictionary1.txt', encoding='utf-8').read().splitlines()
filtered = []
for j, line in enumerate(dictionary):
    '''if re.search(r'.\s*,\s*.', line):
        continue'''
    filtered.append(line)
for lx in filtered:
    print(clear_diacr(lx.split()[0]), [alph.index(x) if x in alph else 1999 for x in clear_diacr(lx.split()[0])])
filtered = sorted(filtered, key=lambda l: [alph.index(x) if x in alph else 1999 for x in clear_diacr(l.split()[0])])

with open('Dictionary1Output.txt', 'w', encoding='utf-8') as d1o:
    d1o.write('\n'.join(filtered))
    d1o.close()