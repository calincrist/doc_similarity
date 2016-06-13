# /usr/bin/python
# -*- coding: utf-8 -*-
"""Module with a class that handles corpora files."""

from __future__ import print_function
import os
import sys
import re
import logging
from logging.config import fileConfig

# Setup logging.
# fileConfig('log_config.ini')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
hdlr = logging.FileHandler('./similarity.log')
log = logging.getLogger()
log.addHandler(hdlr)

reload(sys)
sys.setdefaultencoding('utf8')

BESSARABIA_PATH = 'corpus/years/Bessarabia'
MOLDAVIA_PATH = 'corpus/years/Moldavia'
TRANSILVANYA_PATH = 'corpus/years/Transylvania'
WALLACHIA_PATH = 'corpus/years/Wallachia'

tokenize = lambda doc: doc.lower().split(" ")


class Corpus(object):
    """Class that handles the corpus files."""

    def __init__(self):
        """initialize."""
        # list of paths to all the documents in the corpus
        self.tokenized_romania = []
        self.tokenized_bessarabia = []
        self.tokenized_transylvanian = []
        self.tokenized_wallachian = []
        self.tokenized_moldavian = []

        self.all_romania_documents = []
        self.moldavian_documents = []
        self.wallachian_documents = []
        self.transylvanian_documents = []
        self.all_bessarabia_documents = []

        self.corpus_dir_path = 'corpus'

        self.load_corpus()


    def load_corpus(self):
        """Load corpus."""

        pattern = re.compile('.*\d+.(txt)')
        #   load Bessarabia docs
        for folder, subs, files in os.walk(BESSARABIA_PATH):
            for file in filter(lambda name:pattern.match(name), files):
                self.all_bessarabia_documents.append(os.path.join(BESSARABIA_PATH, file))

        # load Moldavia docs
        # for folder, subs, files in os.walk(MOLDAVIA_PATH):
        #     for file in filter(lambda name:pattern.match(name), files):
        #         self.all_romania_documents.append(os.path.join(MOLDAVIA_PATH, file))
        #         self.moldavian_documents.append(os.path.join(MOLDAVIA_PATH, file))

        # #   load Transylvania docs
        for folder, subs, files in os.walk(TRANSILVANYA_PATH):
            for file in filter(lambda name:pattern.match(name), files):
                self.all_romania_documents.append(os.path.join(TRANSILVANYA_PATH, file))
                self.transylvanian_documents.append(os.path.join(TRANSILVANYA_PATH, file))

        # #   load Wallachia docs
        # for folder, subs, files in os.walk(WALLACHIA_PATH):
        #     for file in filter(lambda name:pattern.match(name), files):
        #         self.all_romania_documents.append(os.path.join(WALLACHIA_PATH, file))
        #         self.wallachian_documents.append(os.path.join(WALLACHIA_PATH, file))


    def tokenize_bessarabia(self):
        """Tokenize Bessarabia files."""
        i = 0
        for path in self.all_bessarabia_documents:
            if i > -1:
                with open(path, 'r') as file_handler:
                    log.info('%d (bes) : %s' % (i, path))
                    text = ''
                    for line in file_handler:
                        line = line.decode('utf-8').strip()
                        line = "".join(c for c in line if
                                       c not in open('separators.txt')
                                       .read()).lower()
                        text += line
                    self.tokenized_bessarabia.append(text)
            else:
                break
            i += 1


    def tokenize_romania(self):
        """Tokenize Romania files."""
        i = 0
        for path in self.all_romania_documents:
            if i > -1:
                with open(path, 'r') as file_handler:
                    log.info('%d (rom) : %s' % (i, path))
                    text = ''
                    for line in file_handler:
                        line = line.decode('utf-8').strip()
                        line = "".join(c for c in line if
                                       c not in open('separators.txt')
                                       .read()).lower()
                        text += line
                    self.tokenized_romania.append(text)
                    self.tokenized_moldavian.append(text)
            else:
                break
            i += 1

        # for path in self.wallachian_documents:
        #     if i > -1:
        #         with open(path, 'r') as file_handler:
        #             log.info('%d (rom) : %s' % (i, path))
        #             text = ''
        #             for line in file_handler:
        #                 line = line.decode('utf-8').strip()
        #                 line = "".join(c for c in line if
        #                                c not in open('separators.txt')
        #                                .read()).lower()
        #                 text += line
        #             self.tokenized_romania.append(text)
        #             self.tokenized_wallachian.append(text)
        #     else:
        #         break
        #     i += 1

        # for path in self.transylvanian_documents:
        #     if i > -1:
        #         with open(path, 'r') as file_handler:
        #             log.info('%d (rom) : %s' % (i, path))
        #             text = ''
        #             for line in file_handler:
        #                 line = line.decode('utf-8').strip()
        #                 line = "".join(c for c in line if
        #                                c not in open('separators.txt')
        #                                .read()).lower()
        #                 text += line
        #             self.tokenized_romania.append(text)
        #             self.tokenized_transylvanian.append(text)
        #     else:
        #         break
        #     i += 1
