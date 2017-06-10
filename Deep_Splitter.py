#!/usr/bin/python3
import re
import pymorphy2
#
#s = 'ақоди /об. Ч/ част. - только: мананэ́л ӣкэк ~ тэтэ́мҗэл под «мое- му сыну-моему только четыре года»; тав қыбачэнд ~ муктэ́т надэллат «этому ребёнку только шесть недель» см. каткабарт ақодя /об. Ш/ ~ ақоҗе /об. Ч/ ~ ақочей /тым./ сущ. - селезень II ақоҗе /об. Ч/ сущ. - селезень; см. ақодя';
#s = 'аза /об. Ш, кет./ отриц. част. - 1) не: со ӱтче ~ тюргун /кет./ «хоро- ший мальчик не плачет»; таб ~ варгын эя /об. Ш/ «он неболь- шой»; мат ~ танвап /об. Ш/ «я не знаю»; 2) нет: ~, мат таптёл ~ тӧнжак /об. Ш/ «нет, я сегодня не приду»; см. а, а^а, ажа II азакау /об. Ш/ сущ. - дедушка аздэ /об. Ч/ сущ. - олень; см. ӓждэ'
#s = 'аввыгу /кет./ отгл. гл., непер., возвр., С - съесться авга /об. Ч/ прил. - короткий: ~ ылбат «короткая жизнь» авгалк /об. Ш/ 1. нареч. необл. - от голода: табла авгалк кумбат /об. Ш/ «они от голода умерли»; 2. сост. ч. имен. сказ.: кат сӯрум авгалң эя /об. Ш/ «зимой зверь голоден»'
s = 'авегом /тым./ ~ авегэ /об. Ч/ отым. сущ. - мачеха авегэ /об. Ч/ отым. сущ. - мачеха; см. авегом авендаз /об. Ш/ сущ. - дедушка (по материнской линии) авес /тур./ сущ. - овес (< русск.)'
def cut(string, title, g_next):
    roman_numerals_regex = r'(I{1,3}|I{0,1}VI{0,3})'
    string = re.sub(r'\n\s*' + roman_numerals_regex + r'\s+', '\n', string)
    string = re.sub(r'\s+' + roman_numerals_regex + r'\s+', ' ', string)
    def occ_dirty(string):
        rx = r'.\s\S+\s+\/[^\/]+\/\s+[^«"]'
        srx = rx[3:]
        first = re.search('^\S+\s+\/[^\/]+\/\s+[^«"]', string).group(0)
        newl = re.findall(r'\n' + srx, string)
        occ = re.findall(rx, string)
        ret = [first] + newl + [x[2:] for x in occ if not x[0] in ('~', ' ')]
        return len(ret) - 1
    def occ_find(string):
        string = string.split('\n')[-1]
        rx = r'.\s\S+\s+\/[^\/]+\/\s+[^«"]'
        first = re.search('^(\s\n)*\S+\s+\/[^\/]+\/\s+[^«"]', string).group(0)
        occ = re.findall(rx, string)
        ret = [first] + [x[2:] for x in occ if not x[0] in ('~', ' ', '\n')]
        return ret
    # recursion
    print(string)
    occ = occ_find(string)
    occd = occ_dirty(string)
    if '\n' in string and string.count('\n') != occd:
        rec = True
        str_sp = string.split('\n')
        add = '\n'.join(str_sp[:-1]) + '\n'
        string = str_sp[-1]
    elif '\n' in string:
        return string
    else:
        add = ''
        rec = False
    #
    def get_left(string):
        rx = r'(?<!~\s)\S+\s+\/[^\/]+\/\s+[^«"]'
        occ = occ_find(string)
        move_left = 8
        focus_word = re.split('\s+', occ[1])[0]
        move_left -= 1
        rx = r'\S+\s+' + rx
        matched = ''
        while re.search(rx, string) and move_left > 0:
            mtch = re.findall(rx, string)
            ms = False
            for m in mtch:
                if focus_word in m:
                    ms = m
                    break
            if not ms:
                break
            rx = r'\S+\s+' + rx
            move_left -= 1
            matched = ms
        return focus_word, matched
    def get_left_w(gl):
        gl_splitted = re.split(r'\s+', gl[1])
        border_index = -1
        while gl_splitted[border_index][0] != '/':
            border_index -= 1
        #if border_index > -3:
        #    return []
        parsed_list = gl_splitted[:border_index]
        left_w = []
        for e in reversed(parsed_list):
            if re.search('^\w+$', e):
                left_w.append(e)
            else:
                break
        return list(reversed(left_w))
    def border_set(depth, left, matched, string, mapping = 'w'):
        # todo: -> mapping
        keyword = left[depth]
        already = False
        new_matched = []
        for e in reversed(matched.split()):
            if e == keyword and not already:
                new_matched.append("\n" + e)
                already = True
            else:
                new_matched.append(e)
        return string.replace (
            matched,
            " ".join(list(reversed(new_matched)))
        )
    def index_by_regex(regex, lst):
        ret = [i for i, e in enumerate(lst) if re.search(regex, e)]
        if len(ret) > 0:
            return ret
        else:
            return False
    #roman_numerals_regex = r'^(I{1,3}|I{0,1}VI{0,3})$'
    gl = get_left(string)
    glsp = re.split(r'\s+', gl[1])[:-3]
    glw = get_left_w(gl)
    def smart_splitter(string, title, g_next, indices = False):
        sp_str = re.split(r'\s+', string)
        # check if there is a russian word
        morph = pymorphy2.MorphAnalyzer()
        stop_newline = False
        ret = []
        ind = 0
        our_ind = False
        for e in reversed(sp_str):
            if 'DictionaryAnalyzer' in str(morph.parse(e)) and not stop_newline:
                ret.append(e + "\n")
                our_ind = ind
                stop_newline = True
            else:
                ret.append(e)
            ind -= 1
        ret = " ".join(ret)
        # there are no russian words => selkup alphabet sorting
        ret = []
        if not stop_newline:
            stop_newline = False
            ind = 0
            our_ind = False
            for e in sp_str:
                if type(g_next) != bool:
                    if e > title and e < g_next:
                        ret.append("\n" + e)
                        our_ind = ind
                    else:
                        ret.append(e)
                else:
                    ret.append(e)
            ind += 1
            ret = " ".join(ret)
        if not indices:
            return ret
        else:
            return our_ind
    if len(glw) == 1:
        return cut(add + border_set(0, glw, gl[1], string), title, g_next)
    elif len(glw) == 2 and glsp[-3] in ('см.', '-'):
        return cut(add + border_set(-1, glw, gl[1], string), title, g_next)
    elif index_by_regex(r'^см\.$', glsp):
        ibr = index_by_regex(r'^см\.$', glsp)[0]
        sec = glsp[ibr + index_by_regex(r'^[^,]*$', glsp[ibr + 1:])[0] + 1:]
        if len(sec) == 2:
            return cut(add + border_set(-1, glw, gl[1], string), title, g_next)
    elif len(glw) >= 3:
        return cut(
            add + border_set(
                smart_splitter(" ".join(glw), title, g_next, True),
                glw, gl[1], string
            ),
            title, g_next
        )
s = 'амырқоль /тур./ отгл. прил. - съедобный амырқоль апсот /тур./ сост. наим - обед'
next = 'амырле'
print(cut(s, 'амырқоль', next ))
