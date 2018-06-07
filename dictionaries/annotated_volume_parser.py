#!/usr/bin/python3
# -*- coding: utf-8 -*
import codecs
import re
import sys
import os
import language_resource_parser
import language_utils
__author__ = "gisly"

class AnnotatedVolumeParser(language_resource_parser.LanguageResourceParser):
    resource_type = 'text'
    resource_language = 'slk'
    result_texts = dict()

    FILE_TYPE_FABULA = 0
    FILE_TYPE_NOTATION = 1
    FILE_TYPE_TITLE = 2
    FILE_TYPE_ALL = 3

    LANGUAGE_CODES = ['en', 'rus', 'slk']

    REPLACEMENT_CHARACTERS = {'к̜':'ӄ', 'К̜':'Ӄ',
                              'Қ' : 'Ӄ',
                              'қ' : 'ӄ',
                              'н̜':'ӈ',
                              'ң' :'ӈ',
                              'Н̜':'Ӈ', 'г̜':'ӷ', 'Г̜':'Ӷ',
                              'и̇':'и̇',
                              '“':'"', '”' : '"',
                              '́ ': '́' ,
                              'ќ' : 'к'}

    """
    parse all files in a directory and write the resulting files into another directory
    """
    def parse_folder(self, folder, output_folder):
        for filename in os.listdir(folder):
            full_filename = os.path.join(folder, filename)
            print("parsing file: % s" % full_filename)
            text_name = filename.split('-')[0]
            file_type, sentences = self.parse_file(full_filename)
            if text_name not in self.result_texts:
                self.result_texts[text_name] = dict()
            self.result_texts[text_name][file_type] = sentences
        self.write_files(output_folder)

    def write_files(self, output_folder):
        for filename, file_info in self.result_texts.items():
            output_filename = os.path.join(output_folder, filename + '.txt')
            print("writing file: %s" % output_filename)
            self.write_file(filename, file_info, output_filename)

    def write_file(self, filename, file_info, output_filename):
        with codecs.open(output_filename, 'w', 'utf-8') as out:
            if self.FILE_TYPE_FABULA in file_info:
                sentences_fabula = file_info[self.FILE_TYPE_FABULA]
                #TODO: do we need the fabula at all?
            if self.FILE_TYPE_NOTATION in file_info:
                sentences_notation = file_info[self.FILE_TYPE_NOTATION]
                for sentence_num, sentence in enumerate(sentences_notation):
                    self.verify_sentence(filename, sentence)
                    out.write(sentence['slk'].strip() + '\r\n')
                    out.write(sentence['rus'].strip() + '\r\n')
                    out.write(sentence['en'].strip() + '\r\n')

                    out.write(sentence['fon'].strip() + '\r\n')
                    out.write(sentence['fon_morph'].strip() + '\r\n')
                    out.write(sentence['gl_rus'].strip() + '\r\n')
                    out.write(sentence['gl_en'].strip() + '\r\n')

    """
    parse a utf-8 file depending on its type
    """
    def parse_file(self, txt_filename):
        if self.is_fabula(txt_filename):
            return self.FILE_TYPE_FABULA, self.parse_fabula(txt_filename)
        if self.is_notation(txt_filename):
            return self.FILE_TYPE_NOTATION, self.parse_notation(txt_filename)
        if self.is_title(txt_filename):
            return self.FILE_TYPE_TITLE, self.parse_title(txt_filename)
        return self.FILE_TYPE_ALL, self.parse_total(txt_filename)

    """
    parse the text (Selkup, Russian, and English lines)
    """
    def parse_fabula(self, txt_filename):
        sentences = []
        last_sentence = None
        last_delimiter = -1
        with codecs.open(txt_filename, 'r', 'utf-8') as fin:
            for line in fin:
                current_sentences, last_sentence, last_delimiter = self.parse_fabula_line(line, last_sentence, last_delimiter)
                sentences += current_sentences
        if last_sentence:
            sentences.append(last_sentence)
        return sentences

    def parse_notation(self, txt_filename):
        sentences = []
        sentence_line_count = 0
        line_rus = None
        line_slk = None
        line_en = None
        line_fon = None
        line_fon_morph = None
        line_gl_rus = None
        line_gl_en = None
        total_line_count = 0
        is_subsentence = False
        with codecs.open(txt_filename, 'r', 'utf-8') as fin:
            for line in fin:
                line = line.strip()
                total_line_count += 1
                if total_line_count <= 2:
                    continue
                if self.is_page_number(line):
                    continue
                if self.is_sentence_start(line):
                    sentence_line_count = 0

                    if line_rus:
                        new_sentence = {'rus': self.preprocess_sentence(line_rus),
                                        'slk': self.preprocess_sentence(line_slk),
                                        'en': self.preprocess_sentence(line_en),
                                        'fon': line_fon, 'fon_morph': line_fon_morph,
                                        'gl_rus': line_gl_rus, 'gl_en': line_gl_en}
                        if is_subsentence:
                            last_sentence = sentences[-1]
                            last_sentence['rus'] += ' ' + new_sentence['rus']
                            last_sentence['slk'] += ' ' + new_sentence['slk']
                            last_sentence['en'] += ' ' + new_sentence['en']
                            last_sentence['fon'] += ' ' + new_sentence['fon']
                            last_sentence['fon_morph'] += ' ' + new_sentence['fon_morph']
                            last_sentence['gl_rus'] += ' ' + new_sentence['gl_rus']
                            last_sentence['gl_en'] += ' ' + new_sentence['gl_en']
                        else:
                            sentences.append(new_sentence)
                        line_rus = None

                    #the sentence is a part of the previous sentence
                    if self.is_subsentence_start(line):
                        is_subsentence = True
                    else:
                        is_subsentence = False
                else:
                    sentence_line_count += 1

                if sentence_line_count == 0:
                    line_fon = line.split('.', 1)[-1]
                elif sentence_line_count == 1:
                    line_fon_morph = line
                elif sentence_line_count == 2:
                    line_gl_en = line
                elif sentence_line_count == 3:
                    line_gl_rus = line
                elif sentence_line_count == 4:
                    line_slk = line
                elif sentence_line_count == 5:
                    line_en = line
                else:
                    line_rus = line
        if line_rus:
            new_sentence = {'rus': line_rus, 'slk': line_slk, 'en': line_en,
                            'fon': line_fon, 'fon_morph': line_fon_morph,
                            'gl_rus': line_gl_rus, 'gl_en': line_gl_en}
            sentences.append(new_sentence)
        return sentences

    """
    parse the line which may be a whole sentence or a part of the previous sentence
    """
    def parse_fabula_line(self, line, current_sentence, delimiter_count):
        line_parts = re.split('(\d+([a-z])*\))', line)

        sentences = []
        for part in line_parts:
            if part is None or part == '' or self.is_page_number(part):
                continue
            #the delimiter is between the Selkup, Russian and English parts
            if self.is_delimiter(part):
                delimiter_count += 1
                if delimiter_count > 2:
                    delimiter_count = 0
            else:
                sentence = self.preprocess_sentence(part)
                if delimiter_count == 0:
                    #it's the Selkup part
                    if current_sentence is not None and not current_sentence['full']:
                        current_sentence['slk'] += ' ' + sentence
                    else:
                        current_sentence = {'slk': sentence, 'rus': '', 'en': '', 'full': False, 'appended': False}
                elif delimiter_count == 1:
                    #it's the English part
                    current_sentence['en'] += ' ' + sentence
                else:
                    #it's the Russian part
                    current_sentence['rus'] += ' ' + sentence
                    current_sentence['full'] = True
                    if not current_sentence['appended']  :
                        sentences.append(current_sentence)
                        current_sentence['appended'] = True

        return sentences, current_sentence, delimiter_count

    """
    replace bad characters, remove unnecessary characters etc
    """
    def preprocess_sentence(self, sentence):
        sentence = sentence.strip()
        for replacement_from, replacement_to in self.REPLACEMENT_CHARACTERS.items():
            sentence = sentence.replace(replacement_from, replacement_to)
        return sentence



    def parse_title(self, txt_filename):
        pass

    def parse_total(self, txt_filename):
        pass

    """
    check if the sentence contains correct characters
    """
    def verify_sentence(self, filename, sentence):
        for language_code in self.LANGUAGE_CODES:
            if self.is_bad(sentence[language_code], language_code):
                raise Exception('Bad %s for sentence %s in %s' % (language_code, sentence[language_code], filename))

    @staticmethod
    def is_fabula(txt_filename):
        return txt_filename.endswith('fabula')

    @staticmethod
    def is_notation(txt_filename):
        return txt_filename.endswith('notation')

    @staticmethod
    def is_title(txt_filename):
        return txt_filename.endswith('title')

    @staticmethod
    def is_delimiter(part):
        return part.strip(')').isnumeric()

    @staticmethod
    def is_page_number(part):
        return re.match('- \d+ -', part.strip()) is not None

    @staticmethod
    def is_subsentence_start(part):
        return re.match('\d+[abcабв](\.|\s)', part) is not None

    @staticmethod
    def is_sentence_start(part):
        return re.match('\d+[abcабв]?(\.|\s)', part) is not None

    @staticmethod
    def is_bad(sentence, language_code):
        return sentence == '' or not language_utils.has_correct_characters(sentence, language_code)

parser = AnnotatedVolumeParser()
parser.parse_folder('.//resources//annotated-vol1',
                    './/resources//annotated-vol1-parsed')