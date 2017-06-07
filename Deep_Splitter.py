#!/usr/bin/python3
import re
import pymorphy2
s = 'ақоди /об. Ч/ част. - только: мананэ́л ӣкэк ~ тэтэ́мҗэл под «мое- му сыну-моему только четыре года»; тав қыбачэнд ~ муктэ́т надэллат «этому ребёнку только шесть недель» см. каткабарт ақодя /об. Ш/ ~ ақоҗе /об. Ч/ ~ ақочей /тым./ сущ. - селезень ақоҗе /об. Ч/ сущ. - селезень; см. ақодя';
def cut(string):
    def get_left(string):
        rx = r'\S+\s+\/[^\/]+\/\s+[^"]'
        occ = re.findall(rx, string)
        # recursion
        if '\n' in string and string.count('\n') != len(occ):
            rec = True
            str_sp = string.split('\n')
            add = '\n'.join(str_sp[:-1])
            string = str_sp[-1]
        elif '\n' in string:
            return string
        else:
            add = ''
            rec = False
        #
        move_left = 4
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
        parsed_list = re.split(r'\s+', gl[1])[:-3]
        left_w = []
        for e in reversed(parsed_list):
            if re.search('^\w+$', e):
                left_w.append(e)
            else:
                break
        return list(reversed(left_w))
    def border_set(depth, left_w, matched, string):
        return string.replace (
            matched, matched.replace(left_w[depth], "\n" + left_w[depth])
        )
    gl = get_left(string)
    glsp = re.split(r'\s+', gl[1])[:-3]
    glw = get_left_w(gl)
    if len(glw) == 1:
        return cut(add + border_set(0, glw, gl[1], string))
    elif len(glw) == 2 and glsp[-3] == 'см.':
        return cut(add + border_set(-1, glw, gl[1], string))

    #print(gl)
    #print(glw)
#print(cut(s))
