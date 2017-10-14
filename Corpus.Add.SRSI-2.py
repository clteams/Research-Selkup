#!/usr/bin/python3
import re
import CorpusUpdate
import pymorphy2

#my_db = CorpusUpdate.Database()
srsi_file = open('resources/srsi-2-plain.txt').read().splitlines()

RX_STOP = r'[\.\?!]$'
RX_USEFUL_START = r'^\s*\d+\s*\.\s*'
RX_PAGE_PATTERN = r'^\s*\d+\s*$'
RX_PAGE_DIV = r'^\s*\d+[^\.]+$'

Buffer = [{}]

StartNum = -1
Mode = 'continue'
Appended = False


def add_to_buffer(num, content, update=False):
    if not num in Buffer[-1]:
        Buffer[-1][num] = []
    if len(Buffer[-1]) == 0:
        Buffer[-1][num].append(content)
    elif len(Buffer[-1]) == 1 and not update:
        Buffer[-1][num].append(content)
    elif len(Buffer[-1]) == 1:
        Buffer[-1][num][-1] += content
    elif len(Buffer[-1]) == 2 and update:
        Buffer[-1][num][-1] += content


def append_on_buffer():
    Buffer.append({})

## I can't use the debugger and therefore I use prints ;)

for line in srsi_file:
    print('-')
    if re.search(RX_USEFUL_START, line):
        print('a')
        Appended = False
        StartNum = int(re.search(r'^\s*(\d+)', line).group(1))
        upd_line = re.sub('^\s*\d+\s*\.\s*', '', line)
        add_to_buffer(StartNum, upd_line)
        Mode = 'started'
    elif (re.search(RX_PAGE_PATTERN, line) or re.search(RX_PAGE_DIV, line)) and not Appended:
        print('b')
        Mode = 'continue'
        Appended = True
        append_on_buffer()
    elif Mode == 'started':
        print('c')
        add_to_buffer(StartNum, line, update=True)
    else:
        print(line)

print(Buffer)