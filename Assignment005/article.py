# -*- coding: utf-8 -*-

import string
import math
import corpus as the_corpus

stop = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

class Article(object):

    def __init__(self, raw, category=None, path=None):
        self._category = category
        self._path = path
        self._raw = raw
        self.update_tf()
        self._tfidf = {}


    def update_tf(self):
        # punc_chars = '’\',"[](){}⟨⟩:،、‒….!‐-?‘’“”;/⁄*&'

        self._tf = {}
        instr = self._raw.lower()
        for char in ['!','(',')','/','\\',',','|','"']:
            instr = instr.replace(char, ' ')

        for key in instr.split():
            key = key.strip(string.punctuation) # Remove puncs at beginning or end
            if (key == '') or (key in stop): continue
            if key in self._tf:
                self._tf[key] += 1
            else:
                self._tf[key] = 1

        return self


    def update_tfidf(self):
        self._tfidf = {}
        corpus = the_corpus.Corpus()
        corpus_size = corpus._size
        corpus_df = corpus._df

        for word, tf in self._tf.iteritems():
            if word in corpus_df:
                df = corpus_df[word]
            else:
                df = 1
            self._tfidf[word] = float(tf) * math.log(corpus_size/float(df), 2)

        return self

    # Dummy function
    computeTFIDF = update_tfidf
