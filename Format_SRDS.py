#!/usr/bin/python3
import pymorphy2
import re

srds = open('./srds2.txt').read().splitlines()

def check_type(string):
    RE_slashG = r'\/\w+\.[^\/]*\/'
    base_patterns = (
        r'\w+\s+[^\/]*' + RE_slashG,
        #/кет./ отгл. гл., пер., С,
        RE_slashG + r'\s+(\s\w\s|\s\w+\.)',
    )
    base_no_patterns = (
        #3) проём: мадан ӓк /об. Ш/ «дверной проём»
        RE_slashG + '\s+[«»]'
    )
    # check for 'base' type
    base_type = True
    for bp in base_patterns:
        if not re.search(bp, string):
            base_type = False
            break
    if base_type:
        for bnp in base_no_patterns:
            if re.search(bnp, string):
                base_type = False
                break
    if not base_type:
        return 'slice' # todo: (maybe) add other types, except base/slice
    else:
        return 'base'
buffer = ''
continue_times = 0
len_srds = len(srds)
for i in range(len(srds)):
    cs = srds[i]
    if continue_times > 0:
        continue_times -= 1
        continue
    if i != len_srds - 1:
        j = i + 1
        while check_type(srds[j]) != 'base':
            cs += srds[j]
            if j == len_srds - 1:
                break
    # remove "err- ors"
    cs = re.sub(r'(?<=[^\s-])-\s', '', cs)

