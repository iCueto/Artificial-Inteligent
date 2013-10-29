#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from corpus import *
from cluster import *
import global_vars as debug


# Dummy function
def computeDocumentFrequency(category_name):
    return Corpus()[category_name].update_df()
def computeTFIDFCategory(category_name):
    return Corpus()[category_name].update_tfidf2()


def cosineSimilarity(tfidf1, tfidf2):
    """
    Compute similarity between two tfidfs.
    """
    common_words = set.intersection(set(tfidf1.keys()), set(tfidf2.keys()))
    s = sum([tfidf1[word]*tfidf2[word] for word in common_words])
    l1 = math.sqrt(sum([f*f for f in tfidf1.values()]))
    l2 = math.sqrt(sum([f*f for f in tfidf2.values()]))
    return float(s)/(l1*l2)


def classify(article):
    """
    classify the given article with all categories.
    Arguments:
    - `raw`: the given article raw text
    """
    sim = [(cosineSimilarity(category._tfidf, article._tfidf), category) for name, category in Corpus()._categories.iteritems()]
    return max(sim)




if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description="""
    Simply use:
    `./ir.py --infile corpus.pickle --classify TARGET_FILE ./`

    Wanzhang Sheng, Copyright 2013, GPL
    """)
    parser.add_argument('source_path',
                        help='The source dir contains all the categories.')
    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Be verbose to debug.")
    parser.add_argument('--infile', dest='infile', help='Load the corpus from pickle.')
    parser.add_argument('--outfile', dest='outfile', help='Save the corpus into pickle.')
    parser.add_argument('--classify', dest='classify_file', help="The file to be classified.")
    args = parser.parse_args()
    debug.VERBOSE = args.verbose


    # Load the corpus
    if args.infile:
        corpus = Corpus().load(args.infile)
    else:
        corpus = Corpus().reset(args.source_path).update()
        if args.outfile: corpus.save(args.outfile)


    # Classify the given file
    if args.classify_file:
        article = Article(read_file(args.classify_file)).update_tfidf()
        res = classify(article)
        print "The file is classified as %s with %f" % (res[1]._name,res[0])


    # hCluster
    s = set()
    # generate for all categories
    for name, category in corpus._categories.iteritems():
        c = Cluster(name, [category])
        s.add(c)
    # merge
    while len(s)>1:
        best = float('-inf')
        best_c1 = None
        best_c2 = None
        for c1 in s:
            for c2 in s:
                if (c1 != c2):
                    sim = cosineSimilarity(c1._tfidf, c2._tfidf)
                    if sim > best:
                        best = sim
                        best_c1 = c1
                        best_c2 = c2
        c = Cluster(("{%s U %s}" % (best_c1._name, best_c2._name)), [best_c1,best_c2])
        s.remove(best_c1)
        s.remove(best_c2)
        s.add(c)
    # get the root
    root = s.pop()
    print root._name
