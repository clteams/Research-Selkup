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

    RUS_SLK_DELIMITER = ' - '
    BAD_SYMBOLS = r'[\[\]\(\),]'

    REPLACEMENT_SYMBOLS = {'|' : 'и', '1': 'и', 'i' : 'и', 'ö' : 'е',
                           'ньщ': 'нщ', 'ньч': 'нч'}

    PREFIX_LIST = {'обез', 'без', 'воз', 'из', 'раз', 'под', 'произ'}

    SELKUP_REPLACEMENT_SYMBOLS = {'-' : '\u0301', 'дж' : 'җ'}

    SPECIAL_SYMBOLS = ['(', ')']

    TYPICAL_NUM_OF_WORDS = 3

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
            rus_keys = sorted(self.result_dict.keys())
            for rus_key in rus_keys:
                slk_descriptions = self.result_dict[rus_key]
                for slk_description in slk_descriptions:
                    fout.write(' '.join(rus_key) + '=' + ' '.join(slk_description) + '\r\n')

    def process_line(self, dict_line):
        line_parts = dict_line.split(self.RUS_SLK_DELIMITER, 1)
        rus_part = self.process_rus(line_parts[0])
        slk_desc_part = self.process_slk_descriptions(line_parts[1], rus_part)
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
        rus_word = self.make_replacements(rus_word, self.REPLACEMENT_SYMBOLS)

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

    @staticmethod
    def make_replacements(rus_word, replacement_table):
        for bad_symbol, good_symbol in replacement_table.items():
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

    def change_prefix(self, rus_word):
        for prefix in self.PREFIX_LIST:
            prefix_hard_sign = prefix + 'ъ'
            prefix_hard_sign_hyphen = prefix_hard_sign + '-'
            if rus_word.startswith(prefix_hard_sign_hyphen):
                return self.process_prefix_hyphen(rus_word, prefix_hard_sign_hyphen)
            if rus_word.startswith(prefix_hard_sign):
                return self.process_prefix(rus_word, prefix_hard_sign)
            if rus_word.startswith(prefix):
                return self.process_prefix(rus_word, prefix)
        return rus_word

    def process_prefix(self, rus_word, prefix):
        current_prefix_len = len(prefix)
        prefix_modified = self.modify_prefix(prefix)
        return prefix_modified + rus_word[current_prefix_len:]

    def process_prefix_hyphen(self, rus_word, prefix):
        current_prefix_len = len(prefix)
        prefix_modified = self.modify_prefix_with_hyphen(prefix)
        return prefix_modified + rus_word[current_prefix_len:]

    @staticmethod
    def modify_prefix(prefix):
        modified_prefix = prefix.strip('ъ')
        if modified_prefix.endswith('з'):
            modified_prefix = modified_prefix[:-1] + 'с'
        return modified_prefix

    @staticmethod
    def modify_prefix_with_hyphen(prefix):
        modified_prefix = prefix.strip('ъ-') + '-'
        return modified_prefix

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

    def process_slk_descriptions(self, slk_desc_part, translation):
        if ' - ' in slk_desc_part:
            print('!!!!!bad word for %s: %s' % (translation, slk_desc_part))
        slk_words = slk_desc_part.strip().split(' ')
        return [self.normalize_selkup_word(word, translation) for word in slk_words]

    def normalize_selkup_word(self, word, translation):
        #TODO: should we remove the markup
        for special_symbol in self.SPECIAL_SYMBOLS:
            if special_symbol in word:
                return word
        return self.transliterate(word, translation)

    def transliterate(self, word, translation):
        word = word.strip('ъ')
        word = self.make_replacements(word, self.SELKUP_REPLACEMENT_SYMBOLS)
        if not language_utils.check_selkup_word(word, translation):
            print('!!!!!!bad check for %s: %s' % (translation, word))
        return word



def process_args():
    if len(sys.argv) < 2:
        raise Exception('usage: grigorovsky_parser filename')

if __name__ == "__main__":
    process_args()
    grigorovsky_parser = GrigorovskyParser()
    grigorovsky_parser.parse_file(sys.argv[1])
