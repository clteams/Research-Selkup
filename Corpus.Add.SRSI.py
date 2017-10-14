#!/usr/bin/python3
import re
import pymorphy2
import string

srsi = open('resources/srsi/full2.txt').read().splitlines()
marked = []
morph = pymorphy2.MorphAnalyzer()
punct = re.escape(string.punctuation)


def get_before_mark(index, step=None):
    if len(marked) == 0:
        return 'nil'
    if step is None:
        step = 1
    return marked[index - step][1]


def get_after_mark(index, step=None):
    if len(marked) == 0:
        return 'nil'
    if step is None:
        step = 1
    return marked[index + step][1]


def is_russian(text):
    splitted = re.split('\s+', text)
    rus = 0
    for token in re.split('\s+', text):
        token = re.sub('[%s]' % (punct), '', token)
        rus_parse = str(morph.parse(token))
        if 'DictionaryAnalyzer' in rus_parse and not 'Unknown' in rus_parse:
            rus += 1

    return (rus / len(splitted)) > 0.4


class Container:
    def __init__(self):
        self.cont = []

    def remove_last(self):
        del self.cont[-1]

    def add_cont(self):
        self.cont.append([])

    def add_line(self, line):
        self.cont[-1].append(line)

    def get_previous_line(self, step=None):
        if step is None:
            step = 1
        try:
            return self.cont[-1][-step][1]
        except IndexError:
            return None


def scan_mark_back(index, mark, step):
    for i in range(1, step + 1):
        if marked[index - i][1] == mark:
            return True
    return False


def scan_mark_forward(index, mark, step):
    for i in range(1, step + 1):
        if marked[index + i][1] == mark:
            return True
    return False

for line in srsi:
    if re.search('^\s*\d+\s*$', line):
        marked.append([line, 'digit'])
    elif 'Сказки и рассказы селькупки Ирины' in line:
        marked.append([line, 'page_pattern'])
    elif re.search('^Текст', line):
        marked.append([line, 'start_text'])
    elif line.isupper():
        marked.append([line, 'title'])
    elif re.search('^\s*[А-ЯЁ]*[а-яё\s]+:', line):
        marked.append([line, 'source'])
    elif re.search('^\s*\d+\s*\.\s*$', line):
        marked.append([line, 'empty_punct_sign'])
    elif re.search('(\s*\d+\.\s*){2,}', line):
        marked.append([line, 'inline_punct_signs'])
    elif re.search('(\s*[А-ЯЁ]\s*\.){2}[А-ЯЁ]', line):
        marked.append([line, 'name'])
    elif re.search('\s*\d+\s*\.\s*[^\t]+', line):
        marked.append([line, 'plain_text:punct'])
    else:
        marked.append([line, 'plain_text'])

COMMENTS_IGNORE = False
BEFORE_NEXT_IGNORE = False

c = Container()
c.add_cont()

for index, line in enumerate(marked):
    if line[1] in ('digit', 'page_pattern', 'empty_punct_sign'):
        continue

    if COMMENTS_IGNORE and line[1] not in ('plain_text:punct', 'title'):
        continue
    elif COMMENTS_IGNORE:
        COMMENTS_IGNORE = False
        #c.add_cont()

    if BEFORE_NEXT_IGNORE and line[1] != 'start_text':
        continue
    else:
        BEFORE_NEXT_IGNORE = False

    if line[1] == 'start_text':
        continue
    try:
        if line[0].strip()[0].islower() and marked[index - 1][1] == 'source' and scan_mark_back(index, 'source', 4):
            COMMENTS_IGNORE = True
    except IndexError:
        pass

    if line[1] == 'title':
        continue

    if line[1] == 'plain_text:punct':
        language = 'rus' if is_russian(line[0]) else 'sel'
        #if not c.get_previous_line() is None and language != c.get_previous_line():
        #    c.add_cont()
        c.add_line([line, language])

    if line[1] == 'source' and scan_mark_forward(index, 'start_text', 4):
        BEFORE_NEXT_IGNORE = True


for a in c.cont[0]:
    print(a)