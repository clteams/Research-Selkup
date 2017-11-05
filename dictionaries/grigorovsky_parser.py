#!/usr/bin/python3
# -*- coding: utf-8 -*
import codecs
import re
import sys
import language_resource_parser
import language_utils
__author__ = "gisly"


class GrigorovskyParser(language_resource_parser.LanguageResourceParser):
    resource_type = 'dict'
    resource_language = 'slk'
    result_dict = dict()

    RUS_SLK_DELIMITER = '-'
    BAD_SYMBOLS = r'[\[\]\(\),]'

    REPLACEMENT_SYMBOLS = {'|' : 'и', '1': 'и', 'i' : 'и', 'ö' : 'е',
                           'ньщ': 'нщ', 'ньч': 'нч'}


    """parse a utf-8 file in the result_dict variable"""
    def parse_file(self, txt_filename):
        with codecs.open(txt_filename, 'r', 'utf-8') as fin:
            prev_line = ''
            for line in fin:
                if not self.RUS_SLK_DELIMITER in line:
                    prev_line += ' ' + line.strip()
                else:
                    if prev_line != '':
                        self.process_line(prev_line)
                    prev_line = line.strip()
            if prev_line != '':
                self.process_line(prev_line)
        txt_filename_out = txt_filename + '_out.txt'
        self.print_dict(txt_filename_out)

    def print_dict(self, txt_filename_out):
        with codecs.open(txt_filename_out, 'w', 'utf-8') as fout:
            keys = sorted(self.result_dict.keys())
            for key in keys:
                slk_descriptions = self.result_dict[key]
                for slk_description in slk_descriptions:
                    fout.write(' '.join(key) + '=' + slk_description + '\r\n')

    def process_line(self, dict_line):
        line_parts = dict_line.split(self.RUS_SLK_DELIMITER, 1)
        rus_part = self.process_rus(line_parts[0])
        slk_desc_part = self.process_slk_descriptions(line_parts[1])
        if rus_part in self.result_dict:
            self.result_dict[rus_part].append(slk_desc_part)
        else:
            self.result_dict[rus_part] = [slk_desc_part]

    def process_rus(self, rus_part):
        rus_part_normalized = self.normalize(rus_part)
        print(rus_part_normalized)
        return rus_part_normalized

    def normalize(self, rus_part):
        rus_words = rus_part.strip().split(' ')
        return tuple([self.normalize_word(word) for word in rus_words])

    def normalize_word(self, rus_word):
        rus_word = rus_word.lower()
        rus_word = re.sub(self.BAD_SYMBOLS, '', rus_word)
        rus_word = rus_word.strip('ъ')
        rus_word = self.make_replacements(rus_word)

        checks = [self.change_ending_sh, self.change_ending_shya,
                  self.change_adj_ending, self.change_prefix,
                  self.change_old_spelling,
                  self.change_ending_verb, self.change_ending_plural, self.change_ending_genitive,
                  self.change_ending_diminutive, self.change_ending_soft_sign, self.change_negative_prefix]
        is_in_dict = language_utils.check_pymorphy(rus_word)
        if is_in_dict:
            return rus_word

        is_in_dict, rus_word = self.check_rus_word_existence(checks, rus_word, 0)

        if not is_in_dict:
            raise Exception("unknown word : " + rus_word)

        return rus_word

    def make_replacements(self, rus_word):
        for bad_symbol, good_symbol in self.REPLACEMENT_SYMBOLS.items():
            rus_word = rus_word.replace(bad_symbol, good_symbol)
        return rus_word

    def check_rus_word_existence(self, checks, original_word, check_number):
        if check_number >= len(checks):
            return False, original_word
        changed_word = checks[check_number](original_word)
        is_in_dict = language_utils.check_pymorphy(changed_word)
        if is_in_dict:
            return True, changed_word
        return self.check_rus_word_existence(checks, original_word, check_number + 1)

    @staticmethod
    def change_ending_sh(rus_word):
        if rus_word.endswith('ш'):
            return rus_word[0:-1] + 'ий'
        if rus_word.endswith('шся'):
            return rus_word[0:-3] + 'ийся'
        return rus_word

    @staticmethod
    def change_ending_shya(rus_word):
        if rus_word.endswith('ше'):
            rus_word = rus_word[0:-2] + 'ние'
        elif rus_word.endswith('шя'):
            rus_word = rus_word[0:-2] + 'ния'
        return rus_word

    @staticmethod
    def change_ending_plural(rus_word):
        if rus_word.endswith('ия'):
            rus_word = rus_word[0:-2] + 'ие'
        elif rus_word.endswith('ыя'):
            rus_word = rus_word[0:-2] + 'ые'
        elif rus_word.endswith('ие'):
            rus_word = rus_word[0:-2] + 'ье'
        return rus_word

    @staticmethod
    def change_ending_genitive(rus_word):
        if rus_word.endswith('аго'):
            rus_word = rus_word[0:-3] + 'ого'
        return rus_word

    @staticmethod
    def change_adj_ending(rus_word):
        if rus_word.endswith('ющий'):
            return rus_word[0:-4] + 'ящий'
        if rus_word.endswith('анный'):
            return rus_word[0:-5] + 'енный'
        if rus_word.endswith('ый'):
            return rus_word[0:-2] + 'ой'
        return rus_word

    @staticmethod
    def change_negative_prefix(rus_word):
        if rus_word.startswith('не'):
            rus_word = 'не ' + rus_word[2:]
        return rus_word

    @staticmethod
    def change_prefix(rus_word):
        if rus_word.startswith('обезъ'):
            return 'обес' + rus_word[5:]
        if rus_word.startswith('обез'):
            return 'обес' + rus_word[4:]
        if rus_word.startswith('безъ'):
            return 'бес' + rus_word[4:]
        if rus_word.startswith('без'):
            return 'бес' + rus_word[3:]
        if rus_word.startswith('возъ'):
            return 'вос' + rus_word[4:]
        if rus_word.startswith('воз'):
            return 'вос' + rus_word[3:]
        if rus_word.startswith('изъ'):
            return 'ис' + rus_word[3:]
        if rus_word.startswith('из'):
            return 'ис' + rus_word[2:]
        if rus_word.startswith('разъ'):
            return 'рас' + rus_word[4:]
        if rus_word.startswith('раз'):
            return 'рас' + rus_word[3:]
        if rus_word.startswith('подъ'):
            return 'под' + rus_word[4:]
        return rus_word

    @staticmethod
    def change_old_spelling( rus_word):
        return language_utils.change_old_spellings(rus_word)

    @staticmethod
    def change_ending_verb( rus_word):
        if rus_word.endswith('ть'):
            rus_word = rus_word[0:-2] + 'т'
        return rus_word

    @staticmethod
    def change_ending_diminutive( rus_word):
        if rus_word.endswith('ок'):
            rus_word = rus_word[0:-2] + 'ек'
        elif rus_word.endswith('ек'):
            rus_word = rus_word[0:-2] + 'ок'
        return rus_word

    @staticmethod
    def change_ending_soft_sign(rus_word):
        if rus_word.endswith('чь'):
            return rus_word[0:-2] + 'ч'
        return rus_word

    def process_slk_descriptions(self, slk_desc_part):
        #TODO:
        return slk_desc_part

def process_args():
    if len(sys.argv) < 2:
        raise Exception('usage: grigorovsky_parser filename')

if __name__ == "__main__":
    process_args()
    grigorovsky_parser = GrigorovskyParser()
    grigorovsky_parser.parse_file(sys.argv[1])
