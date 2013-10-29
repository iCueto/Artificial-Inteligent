HIGHEST_SCORE_WORDS = 1000

class Category(object):

    def __init__(self, name, corpus=None):
        self._name = name
        self._corpus = corpus
        self._articles = []
        self._df = {}
        self._tfidf = {}


    def update_df(self):
        self._df = {}

        for article in self._articles:
            for word, freq in article._tf.iteritems():
                if word in self._df:
                    self._df[word] += 1
                else:
                    self._df[word] = 1

        return self


    # by highest 1000 TFIDF of articles after merge
    def update_tfidf(self):
        self._tfidf = {}

        for article in self._articles:
            for word, a_tfidf in article._tfidf.iteritems():
                if word in self._tfidf:
                    self._tfidf[word] += a_tfidf
                else:
                    self._tfidf[word] = a_tfidf

        dictlist = sorted(self._df.keys(), key=self._df.__getitem__)
        dictlist = dictlist[-HIGHEST_SCORE_WORDS:]
        self._tfidf = { word: self._tfidf[word] for word in dictlist }
        return self
