#!/usr/bin/env python
# coding=utf-8

"""Language similarity using doc2vec."""
import csv
import os
import collections
from collections import defaultdict
from gensim import corpora, models, similarities
from corpora import Corpus

import logging
from logging.config import fileConfig

# Setup logging.
# fileConfig('log_config.ini')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
hdlr = logging.FileHandler('./similarity.log')
log = logging.getLogger()
log.addHandler(hdlr)

log.info('Start!')


corpuss = Corpus()
# corpuss.tokenize_bessarabia()
corpuss.tokenize_romania()
big_corpus = corpuss.tokenized_romania #+ corpuss.tokenized_romania

# log.info('Big corpus: %s' % big_corpus)

# remove common words and tokenize
stoplist = set('această intru preste față făcut foarte fostu nóstre despre sale dara anulu inse alta cele sunt fara prin dupa cari aceasta sînt fără toate între după acii '\
'cãtre decît suntu dein loru dela numai voru catu totu suntu acésta celu inca pndia pana acésta' \
'tóte carea acesta tote candu intre dectu multu pote acestu nici tóte fost póte'.split())
log.info(stoplist)
texts = [[word for word in document.lower().split() if ((len(word) > 3) and (word.encode('utf-8') not in stoplist))]
         for document in big_corpus]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
         for text in texts]
# pprint(texts)

dictionary = corpora.Dictionary(texts)
# store the dictionary, for future reference
dictionary.save('./output/deerwester.dict')
# pprint(dictionary.token2id)

corpus = [dictionary.doc2bow(text) for text in texts]
# store to disk, for later use
corpora.MmCorpus.serialize('./output/deerwester.mm', corpus)
# pprint(corpus)

dictionary = corpora.Dictionary.load('./output/deerwester.dict')
corpus = corpora.MmCorpus('./output/deerwester.mm')
# log.info('mm[0]: %s' % corpus[14])

tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
corpus_tfidf = tfidf[corpus]  # step 2 -- use the model to transform vectors
# for doc in corpus_tfidf:
#     print(doc)

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)
lsi.show_topics(num_topics=-1, num_words=10, log=False, formatted=False)

def write_csv(csv_title, row_years_list, values_dict):
    """Write to csv file."""
    f = open(csv_title, 'at')
    try:
        writer = csv.writer(f, dialect='excel')
        row = ('----',)

        row_years_list.sort()
        for year in row_years_list:
            row += (year,)
        writer.writerow(row)

        for year2, value_list in values_dict.items():
            row = (year2, )
            for year1 in row_years_list:
                for obj in value_list:
                    if year1 in obj:
                        row += (obj[year1],)
                        break
            writer.writerow(row)
    finally:
        f.close()


def construct_matrix(scores, year1):
    row_years.append(year1)

    for similarity_tuple in scores:
        year2 = corpuss.all_romania_documents[int(similarity_tuple[0])][-8:-4]
        value = {
            year1: similarity_tuple[1]
        }
        if vals[year2]:
            vals[year2].append(value)
        else:
            vals[year2] = [value]


def compute_similarity(document_to_measure, year1):
    """Compute similarities between documents."""
    vec_bow = dictionary.doc2bow(document_to_measure.lower().split())
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space
    # print("vec_bow :")
    # log.info('vec_lsi: %s' % vec_lsi)

    # transform corpus to LSI space and index it
    index = similarities.MatrixSimilarity(lsi[corpus])
    index.save('./output/deerwester.index')
    index = similarities.MatrixSimilarity.load('./output/deerwester.index')

    # perform a similarity query against the corpus
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])


    # print (document_number, document_similarity) 2-tuples
    # print(list(enumerate(sims)))

    # print("sims")
    # pprint(sims)  # print sorted (document number, similarity score) 2-tuples
    construct_matrix(sims, year1)


# row_years = []
# vals = collections.defaultdict(type(''))
# for index, doc in enumerate(corpuss.tokenized_bessarabia):
#     compute_similarity(doc, corpuss.all_bessarabia_documents[index][-8:-4])
# write_csv('moldavia' + '.csv', row_years, vals)

# row_years = []
# vals = collections.defaultdict(type(''))
# for index, doc in enumerate(corpuss.tokenized_bessarabia):
#     compute_similarity(doc, corpuss.all_bessarabia_documents[index][-8:-4])
# write_csv('wallachia' + '.csv', row_years, vals)

# row_years = []
# vals = collections.defaultdict(type(''))
# for index, doc in enumerate(corpuss.tokenized_bessarabia):
#     compute_similarity(doc, corpuss.all_bessarabia_documents[index][-8:-4])
# write_csv('transylvania' + '.csv', row_years, vals)



# verificare distante in interiorul corpusului
# topics / an
# topics / regiune
