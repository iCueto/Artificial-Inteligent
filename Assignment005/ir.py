#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle
import os,sys
from os import listdir
from os.path import isfile, join
import string
import re
import math
import argparse


HIGHEST_SCORE_WORDS = 1000


def strip(target_string, exclusive_chars=None):
    """
    Remove all exclusive_chars at the beginning or the end of the string.
    """
    #return target_string.strip(exclusive_chars)
    return target_string.strip(string.punctuation)


# punctuations = {'’','\'',',','"','[',']','(',')','{','}','⟨','⟩',':','،','、','‒','…','.','!','‐','-','?','‘','’','“','”',';','/','⁄','*','&'}
# punc_chars = '’\',"[](){}⟨⟩:،、‒….!‐-?‘’“”;/⁄*&'
punc_chars = '’\',"[](){}⟨⟩:،、‒….!?‘’“”;/⁄*&' # Remove hyphen punc

def wordfreq(instr, wf=None, stripPunc=True, toLower=True) :
    if not wf: wf = {}
    if toLower: instr = instr.lower()
    if stripPunc: instr = instr.replace('!',' ')\
                               .replace('(',' ').replace(')',' ')\
                               .replace('/',' ').replace('\\',' ')\
                               .replace(',',' ')\
                               .replace('|',' ')\
                               .replace('"',' ')

    for key in instr.split():
        if stripPunc: key = strip(key, punc_chars)
        if key == '': continue
        if key in wf:
            wf[key] += 1
        else:
            wf[key] = 1

    return wf


class Category(object):
    """
    Category Class store the category IDF dict.
    """

    def __init__(self, name):
        """
        Init category name.
        Arguments:
        - `name`:
        """
        self._name = name
        self._articles = []
        self._idf = {}
        self._tfidf = {}

    def update_df(self):
        """
        Return DF of words occurs in this category.
        """
        self._idf = {}
        for article in self._articles:
            for word, freq in article._tf.iteritems():
                if word in self._idf:
                    self._idf[word] += 1
                else:
                    self._idf[word] = 1
        return self._idf

    def update_tfidf(self):
        """
        Update highest TFIDF words.
        """
        dictlist = sorted(self._idf.keys(), key=self._idf.__getitem__)
        dictlist = dictlist[-HIGHEST_SCORE_WORDS:]
        self._tfidf = { word: 0 for word in dictlist }

        for article in self._articles:
            for word, a_tfidf in article._tfidf.iteritems():
                if word in self._tfidf:
                    self._tfidf[word] += a_tfidf

        # TODO pickle
        return self._tfidf


class Article(object):
    """
    Article Class stores the category (newsgroup name) of an article,
    a string containing its raw text,
    and a dictionary that maps words (except stopwords and non-words) to their TFIDF score.
    """

    def __init__(self, category, raw):
        """
        Parse article when init.
        Arguments:
        - `category`: article's category
        - `raw`: raw text of the article
        """
        self._category = category
        self._raw = raw
        self._tf = wordfreq(raw)
        self._tfidf = {}

    def computeTFIDF(self):
        """
        Compute TFIDF for this article.
        """
        self._tfidf = {}
        for word, tf in self._tf.iteritems():
            c = category_by_name(self._category)
            idf = c._idf[word]
            # TODO is corpus means category DF?
            self._tfidf[word] = float(tf) * math.log(len(c._articles)/float(idf))
        return self._tfidf


def category_by_name(name):
    """
    return category by name
    Arguments:
    - `name`: the name of category
    """
    return categories[name]


def read_file(category, filename):
    """
    Create article from file.
    Arguments:
    - `category`: category of the file
    - `filename`: the input file path
    """
    try:
        infile = open(filename, 'r')
        instr = infile.read()
    except:
        SystemExit('[ERROR] Read the %s!' % filename)
    finally:
        infile.close

    return Article(category, instr)


def computeDocumentFrequency(category_name):
    """
    Compute DF by category_name.
    """
    return category_by_name(category_name).update_df()


def cosineSimilarity(tfidf1, tfidf2):
    """
    Compute similarity between category1 and category2
    """
    return 'todo'


def test_articles_key_with_pattern(articles):
    for article in articles:
        for k,v in article._tf.iteritems():
            if not re.match('^[\w\-\.\'\:\@\+]+$', k):
                print k


if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description="""
    TFIDF:
    Based on 20 NewsGroups to analysis similarities.
    Ranmocy Sheng, Copyright 2013, GPL
    """)
    parser.add_argument('source_path', help='The source dir contains categories.')
    # parser.add_argument('--nostrip', dest='stripPunc', action='store_false',
    #                    help='if --nostrip, don\'t strip punctuation')
    # parser.add_argument('--noConvert', dest='toLower', action='store_false',
    #                    help='if --noConvert, don\'t convert everything to lower case')
    # parser.add_argument('--outfile', dest='outfile',
    #                    help='if --pfile=outfile, pickle the resulting dictionary and store it in outfile. otherwise, print it to standard out.')

    args = parser.parse_args()


    # Get the categories list
    print "Reading the categories..."
    categories = {}
    for f in listdir(args.source_path):
        if not isfile(join(args.source_path, f)):
            categories[f] = Category(f)
    print "%d categories found." % len(categories)


    # Read files
    for name, c in categories.iteritems():
        print "Reading the files in %s" % name
        for f in listdir(join(args.source_path, name)):
            path = join(args.source_path, name, f)
            if isfile(path):
                c._articles.append(read_file(name, path))


    # compute IDF
    for name, c in categories.iteritems():
        print "Compute IDF for category %s" % name
        computeDocumentFrequency(name)


    # compute TFIDF
    for name, c in categories.iteritems():
        print "Compute TFIDF for articles in %s" % name
        for article in c._articles:
            article.computeTFIDF()


    # compute TFIDF for category
    for name, c in categories.iteritems():
        print "Compute TFIDF of category %s" % name
        c.update_tfidf()
