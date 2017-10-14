#!/usr/bin/python3
import re
import CorpusUpdate
import selkup_alphabet

my_db = CorpusUpdate.Database()
srsi_file = open('resources/srsi-2-plain.txt').read().splitlines()

RX_STOP = r'[\.\?!]$'
RX_USEFUL_START = r'^\s*\d+\s*\.\s*'
RX_PAGE_PATTERN = r'^\s*\d+\s*$'
RX_PAGE_DIV = r'^\s*\d+[^\.]+$'

Buffer = [{}]

StartNum = -1
Mode = 'continue'
Appended = False


def content_handler(on, what):
    on = on.strip()
    what = what.strip()
    if re.search('-$', on):
        on = on[:-1]
    else:
        on += ' '
    return on + what


def add_to_buffer(num, content, update=False):
    if not num in Buffer[-1]:
        Buffer[-1][num] = []
    if len(Buffer[-1][num]) == 0:
        Buffer[-1][num].append(content)
    elif len(Buffer[-1][num]) == 1 and not update:
        Buffer[-1][num].append(content)
    elif len(Buffer[-1][num]) == 1:
        Buffer[-1][num][-1] = content_handler(Buffer[-1][num][-1], content)
    elif len(Buffer[-1][num]) == 2 and update:
        try:
            Buffer[-1][num][-1] = content_handler(Buffer[-1][num][-1], content)
        except IndexError:
            print(Buffer)
            raise ValueError()


def append_on_buffer():
    Buffer.append({})


for line in srsi_file:
    if re.search(RX_USEFUL_START, line):
        Appended = False
        StartNum = int(re.search(r'^\s*(\d+)', line).group(1))
        upd_line = re.sub('^\s*\d+\s*\.\s*', '', line)
        add_to_buffer(StartNum, upd_line)
        Mode = 'started'
    elif (re.search(RX_PAGE_PATTERN, line) or re.search(RX_PAGE_DIV, line)) and not Appended:
        Mode = 'continue'
        Appended = True
        append_on_buffer()
    elif Mode == 'started':
        add_to_buffer(StartNum, line, update=True)
    else:
        if not Appended:
            append_on_buffer()
            Appended = True
        Mode = 'continue'

srsi_strict = selkup_alphabet.Conv.srsi.strict

for BufferSection in Buffer:
    bsl = len(BufferSection)
    for Index in BufferSection:
        prepare = {
            'text.selkup': selkup_alphabet.Conv.Methods.unify(
                BufferSection[Index][0],
                strict=srsi_strict,
                soft=[],
                strict_only=True
            ),
            'lemmatized.selkup': ['_' for _ in range(len(BufferSection[Index][0]))],
            'text.russian': BufferSection[Index][1],
            'metadata.source': ['SRSI_2_'],
            'metadata.date': ['10/14/2017'],
            'metadata.pushed_by': ['admin']
        }
        if Index != bsl - 1:
            prepare['metadata.sequence'] = ['true']
        my_db.add_segment(prepare)

my_db.commit()
my_db.close()