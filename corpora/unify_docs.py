#!/usr/bin/env python
# -- coding: utf-8 --

import re
import os
import sys
import logging
import collections

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
log = logging.getLogger()

BESSARABIA_PATH = '../corpus/Bessarabia'
MOLDAVIA_PATH = '../corpus/Moldavia'
TRANSILVANYA_PATH = '../corpus/Transylvania'
WALLACHIA_PATH = '../corpus/Wallachia'

"""
files = {
    region1: {
        year1 : [file1, file 2, ...],
        year2 : [file1, file 2, ...],
        year3 : [file1, file 2, ...],
        ...
    },
    region2: {
        year1 : [file1, file 2, ...],
        year2 : [file1, file 2, ...],
        year3 : [file1, file 2, ...],
        ...
    },
    ...
}
"""
docs_per_year = collections.defaultdict(type(''))


def get_docs_per_region(region_path):
    pattern = re.compile('.*\d+.(txt)')
    region_years = collections.defaultdict(lambda: [])
    #   load Bessarabia docs
    for folder, subs, files in os.walk(region_path):
        for file in filter(lambda name: pattern.match(name), files):    
            region_years[file[-8:-4]].append(file)
    docs_per_year[region_path] = region_years


def get_docs_per_year():
    get_docs_per_region(BESSARABIA_PATH)
    get_docs_per_region(MOLDAVIA_PATH)
    get_docs_per_region(TRANSILVANYA_PATH)
    get_docs_per_region(WALLACHIA_PATH)


def concatenate_docs(region, filenames, year):
    output_filename = os.path.abspath('../corpus/years/%s/%s.txt' % (region, year))
    outfile = open(output_filename, 'a+', encoding='latin1')
    for fname in filenames:
        fname = '../corpus/' + region + '/' + fname
        with open(fname, encoding='latin1') as infile:
            for line in infile:
                outfile.write(line)
    outfile.close()


get_docs_per_year()
for path, files_list in docs_per_year.items():
    log.info(path)
    region = os.path.basename(os.path.normpath(path))
    for year, files in files_list.items():
        concatenate_docs(region, files, year)
