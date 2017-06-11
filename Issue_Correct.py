#!/usr/bin/python3
import re
i = open('srds-formatted.txt').read()
out = 'srds-corrected.txt'

# rsi 22
i = re.sub(r'(?<=\w)/', ' /', i)

with open(out, 'w') as o:
    o.write(i)

