#!/usr/bin/python3
import re

srds = open('./srds2.txt').read().splitlines()

output_name = './srds-semi-formatted.txt' # example name

# todo: check if the newline symbol is required

with open(output_name, 'a') as o:
    for s in srds:
        o.write(re.sub('\s{2,}', ' ', s))

