# encoding: utf-8

import inquirer
import re
import os
from google.cloud import translate_v2 as translate


class Translator:
    def __init__(self, answers_prompt):
        self.answers = answers_prompt
        self.dict = {
            'Arabe': 'ar',
            'Alemao': 'de',
            'Espanhol': 'es',
            'Estoniano': 'et',
            'Frances': 'fr',
            'Ingles': 'en',
            'Holandes': 'nl',
            'Japones': 'ja',
            'Portugues': 'pt'
        }
        self.regex = r"\w+:.(['])(?:(?=(\\?))\2.)*?\1"
        self.to_be_translated = ''
        self.has_written_head = False
        self.index = 1
        self.file_length = 0
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.answers['api']
        self.client = translate.Client()

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' or os.name == 'dos' else 'clear')

    def print_info(self, index, file):
        self.cls()
        print('Traduzindo {index}/{len} - {file}.js'.format(index=index, len=self.file_length, file=file))

    def read_file(self):
        with open(self.answers['path'], 'r', encoding='utf-8') as reader:
            lines = reader.read()
        self.get_words_and_meaning(lines)

    def get_words_and_meaning(self, text):

        self.file_length = len(tuple(re.finditer(self.regex, text, re.MULTILINE)))
        for lang in self.answers['dest_lang']:
            matches = re.finditer(self.regex, text, re.MULTILINE)
            for match in matches:
                match_group = match.group().split(':')
                self.translate_word(match_group[0], match_group[1].replace('\'', ''), self.dict[lang])
            self.index = 1
            self.has_written_head = False

    def translate_word(self, key, phrase, target):
        self.print_info(self.index, target)
        result = self.client.translate(phrase, target_language=target,
                                       source_language=self.dict[self.answers['source_lang']])
        self.write_to_file(key, result['translatedText'], target+'.js')

    @staticmethod
    def clear_file(file):
        open(file, 'w').close()

    def write_file_head(self, file_name):
        self.clear_file(file_name)
        with open(file_name, 'a', encoding='utf-8') as writer:
            writer.write('export default {\n')

    def write_to_file(self, key, text, file_name):
        if not self.has_written_head:
            self.write_file_head(file_name)
            self.has_written_head = True
        should_have_comma = ','
        is_last_line = self.index == self.file_length
        if is_last_line:
            should_have_comma = ''
        with open(file_name, 'a', encoding='utf-8') as writer:
            writer.write('  {key}: \'{text}\'{comma}\n'.format(key=key, text=text, comma=should_have_comma))
            self.index += 1
        if is_last_line:
            self.write_file_tail(file_name)

    @staticmethod
    def write_file_tail(file_name):
        with open(file_name, 'a', encoding='utf-8') as writer:
            writer.write('}')


questions = [
    inquirer.Text('api',
                  message='Caminho para chave de serviço (Ex: ./gcp-test-208916-68785fc22a67.json)',
                  default=''),
    inquirer.List('source_lang',
                  message='Em qual lingua do arquivo original? ',
                  choices=['Arabe', 'Alemao', 'Espanhol', 'Estoniano', 'Frances', 'Ingles', 'Holandes',
                           'Japones',
                           'Portugues']),
    inquirer.Checkbox('dest_lang',
                      message='A traducao deve ser feita para quais linguas? ',
                      choices=['Arabe', 'Alemao', 'Espanhol', 'Estoniano', 'Frances', 'Ingles', 'Holandes',
                               'Japones', 'Portugues']),
    inquirer.Text('path',
                  message='Qual o nome do arquivo a ser traduzido? (Ex: ./pt.js)',
                  default='')
]
answers = inquirer.prompt(questions)
# answers = {'api': './gcp-test-208916-68785fc22a67.json', 'source_lang': 'Portugues', 'dest_lang': ['Arabe', 'Alemao', 'Espanhol'], 'path': './pt.js'}

tradutor = Translator(answers)
tradutor.read_file()

