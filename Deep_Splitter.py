#!/usr/bin/python3
import re
import pymorphy2
#
s = open('tests/ds2').read()
#
class reg:
    w = r'[\wёқэ́ӓҗӣңёӧи́ӯӱ]'
    w_lex = w[:-1] + r'\s~]+'
def cut(string, title, g_next):
    debug = False
    roman_numerals_regex = r'(I{1,3}|I{0,1}VI{0,3})'
    string = re.sub(r'\n\s*' + roman_numerals_regex + r'\s+', '\n', string)
    string = re.sub(r'\s+' + roman_numerals_regex + r'\s+', ' ', string)
    string = re.sub(r'/[^/]+/', '/J/', string)
    def occ_dirty(string):
        rx = r'.\s\S+\s+\/[^\/]+\/\s+[^«"]'
        srx = rx[3:]
        first = re.search(r'^' + reg.w_lex + r'\/[^\/]+\/\s+[^«"]', string).group(0)
        newl = re.findall(r'\n' + srx, string)
        occ = re.findall(rx, string)
        ret = [first] + newl + [x[2:] for x in occ if not x[0] in ('~', ' ')]
        return len(ret) - 1
    def occ_find(string):
        string = string.split('\n')[-1]
        rx = r'.\s\S+\s+\/[^\/]+\/\s+[^«"]'
        first = re.search('^(\s\n|\s)*' + reg.w_lex + r'\/[^\/]+\/\s+[^«"]', string).group(0)
        occ = re.findall(rx, string)
        ret = [first] + [x[2:] for x in occ if not x[0] in ('~', ' ', '\n')]
        return ret
    # recursion
    occ = occ_find(string)
    if len(occ) == 1:
        return string	
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
            if re.search(r'^' + reg.w + r'+$', e):
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
    first_title = re.search(r'^' + reg.w_lex + r'(?=\/[^\/]+\/\s+[^«"])', string).group(0)
    new_title = first_title.replace(' ', '')
    t_space = False
    t_space = len(first_title.split()) != 1
    if t_space:
        string = re.sub(r'^' + reg.w_lex + r'(?=\/[^\/]+\/\s+[^«"])', new_title, string)    
    gl = get_left(string)
    glsp = re.split(r'\s+', gl[1])[:-2]
    glw = get_left_w(gl)
    def smart_splitter(string, title, g_next, indices = False):
        def to_cyr(s):
            rep1 = 'қ э́ ӓ җ ӣ ң ё ӧ и́ ӯ ӱ'.split()
            rep2 = 'к э а ж и н е о и у у'.split()
            for j in range(len(rep1)):
                s = s.replace(rep1[j], rep2[j])
            return s
        sp_str = re.split(r'\s+', string)
        # check if there is a russian word
        morph = pymorphy2.MorphAnalyzer()
        stop_newline = False
        ret = []
        ind = 0
        our_ind = False
        for i in range(len(sp_str) - 1, -1, -1):
            e = sp_str[i]
            str_parse = str(morph.parse(e))
            if 'DictionaryAnalyzer' in str_parse and not 'Unknown' in str_parse and not stop_newline:
                ret.append(e + "\n")
                our_ind = ind
                stop_newline = True
            else:
                ret.append(e)
            ind -= 1
        ret = " ".join(reversed(ret))
        # there are no russian words => selkup alphabet sorting
        if not stop_newline:
            alph_sorting = False
            ret = []
            stop_newline = False
            ind = 0
            our_ind = False
            for e in sp_str:
                if type(g_next) != bool:
                    if to_cyr(e) >= to_cyr(title) and to_cyr(e) <= to_cyr(g_next):
                        ret.append("\n" + e)
                        our_ind = ind
                        alph_sorting = True
                    else:
                        ret.append(e)
                else:
                    ret.append(e)
                ind += 1
            ret = " ".join(ret)
        if not alph_sorting:
            def i_simil(a, b):
                a = re.split(r'\s+', a)[0]
                b = re.split(r'\s+', b)[0]
                s = 0
                try:
                    while a[s] == b[s]:
                        s += 1
                except IndexError:
                    return s
                return s
            ret = []
            stop_newline = False
            results = []
            for e in sp_str:
                results.append(i_simil(e, g_next))
            def find_max_ind(l):
                m = -1
                ix = -1
                for i in range(len(l)):
                    if l[i] > m:
                        m = l[i]
                        ix = i
                return ix
            our_ind = find_max_ind(results)
            ret = []
            for i in range(len(sp_str)):
                if i != our_ind:
                    ret.append(sp_str[i])
                else:
                    ret.append("\n" + sp_str[i])
            ret = " ".join(ret)
        ret = re.sub(r'\n\s+', '\n', ret)
        if not indices:
            return ret
        else:
            return our_ind
    ret = False
    if len(glw) == 1:
        if debug:
            print('parsing mode: 1')
        ret = add + border_set(0, glw, gl[1], string)
    elif len(glw) == 2 and glsp[-3] in ('см.', '-'):
        if debug:
            print('parsing mode: 2')
        ret = add + border_set(-1, glw, gl[1], string)
    elif index_by_regex(r'^см\.$', glsp):
        if debug:
            print('parsing mode: 3')
        ibr = index_by_regex(r'^см\.$', glsp)[0]
        sec = glsp[ibr + index_by_regex(r'^[^,]*$', glsp[ibr + 1:])[0] + 1:]
        if len(sec) == 2:
            if debug:
                print('parsing mode: 3A')
            ret = add + border_set(-1, glw, gl[1], string)
        else:
            if debug:
                print('parsing mode: 3B')
            j_glw = " ".join(glw)
            ret = add + string.replace(j_glw, smart_splitter(j_glw, title, g_next))
    elif len(glw) >= 3:
        if debug:
            print('parsing mode: 4')
        j_glw = " ".join(glw)
        ret = add + string.replace(j_glw, smart_splitter(j_glw, title, g_next))
    if ret:
        if t_space:
            ret = ret.replace(new_title, first_title)
        return cut(ret, title, g_next)
    else:
        raise ValueError('')
strs = s.splitlines()
first_s = []
for s in strs:
    first_s.append(re.search(r'^(\s\n|\s)*' + reg.w[:-1] + r'\s]' + r'+', s).group(0))
    first_s[-1] = re.sub(r'\s+$', '', first_s[-1])
for j in range(len(strs)):
    strs_j = strs[j]
    q_occs = re.finditer(r'\s+~\s+(\w+\s*)+(?=\s+\/)', strs_j)
    m_occs = re.finditer(r'/[^/]+/', strs_j)
    strs_j = re.sub(r'\s+~\s+(\w+\s*)+(?=\s+\/)', 'Q', strs_j)
    if len(re.findall(reg.w_lex + r'\s+\/[^\/]+\/\s+[^«"]', strs_j)) > 1:
        strs_j = re.sub(r'\s(I+|I*VI*)\s|^(I+|I*VI*)\s|\s(I+|I*VI*)$', ' ', strs_j)
        if j == len(strs) - 1:
            g_next = False
        else:
            g_next = first_s[j + 1]
        res = cut(strs_j, first_s[j], g_next)
    else:
        res = strs_j
    for qo in q_occs:
        res = res.replace('Q', qo.group(0), 1)
    for mo in m_occs:
        res = res.replace('/J/', mo.group(0), 1)
    print(res)