#!/usr/bin/python3
import pymorphy2
import re

#srds = open('./srds2.txt').read().splitlines()
srds = open('tests/f5').read().splitlines()

def check_type(string):
    RE_slashG = r'\/\w+\.[^\/]*\/'
    base_patterns = (
        r'\w+\s+[^\/]*' + RE_slashG,
        #/кет./ отгл. гл., пер., С,
        RE_slashG + r'\s+(\s\w\s|\s\w+\.)',
    )
    base_no_patterns = (
        #3) проём: мадан ӓк /об. Ш/ «дверной проём»
        RE_slashG + r'\s+[«»]',
	#2. соответствует отриц. приставке «не»
	r'^\s*\d+\.'
    )
    # check for 'base' type
    base_type = False
    for bp in base_patterns:
        if re.search(bp, string):
            base_type = True
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
            cs += " " + srds[j]
            if j == len_srds - 1:
                break
            j += 1
            continue_times += 1
    # remove "err- ors"
    cs = re.sub(r'(?<=[^\s-])-\s', '', cs)
    # `^ -> 'гх'` 2017-06-10 issue
    cs = re.sub(r'\^', 'гх', cs)
    # `rsi 18` issue [not full]
    cs = re.sub(r'(?<=\w)\d', 'гх', cs)
    # `rsi 19` issue
    cs = re.sub(r'(/[^\/]+/)(\d+)', '\g<1> \g<2>', cs)
    # `rsi 21` issue
    cs = re.sub(r'(?<=\w)[\d;]+', 'дф', cs)
    cs = re.sub(r'[\d;]+(?=\w)', 'дф', cs)
    print(cs)

