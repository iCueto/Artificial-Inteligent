import cPickle as pickle
import os,sys
from os import listdir
from os.path import isfile, join

from category import *
from article import *
import global_vars as debug


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class Corpus(object):
    __metaclass__ = Singleton

    def __init__(self):
        if not hasattr(self, '_root'): self._root = None
        self._categories = {}
        self._size = 0
        self._df = {}


    def __getitem__(self, category_name):
        return self._categories[category_name]


    def reset(self, root=None):
        self.__init__()
        if root: self._root = root
        return self


    def save(self, outfile='corpus.pickle'):
        try:
            f = open(outfile, 'wb')
            if debug.VERBOSE: print "Saving to %s" % outfile
            pickle.dump(self, f)
            f.close()
        except Exception as e:
            print '[ERROR] Can not write to outfile!'
            print 'Error massage:'
            print e
        return self


    def load(self, infile='corpus.pickle'):
        try:
            f = open(infile, 'rb')
            if debug.VERBOSE: print "Loading from %s" % infile
            p = pickle.load(f)
            Corpus._instances[Corpus] = p
            self = p
            f.close()
        except Exception as e:
            print '[ERROR] Can not read from infile.'
            print 'Error massage:'
            print e
        return self


    def update_size(self):
        if debug.VERBOSE: print "Updateing corpus size"
        self._size = sum([len(c._articles) for k, c in self._categories.iteritems()])
        return self


    def update_df(self):
        if debug.VERBOSE: print "Updating corpus DF"
        self._df = {}
        for n, c in self._categories.iteritems():
            self._df.update(c._df)
        return self


    def scan(self):
        root_path = self._root

        # Get the categories list
        if debug.VERBOSE: print "Reading the categories..."
        for name in listdir(root_path):
            if not isfile(join(root_path, name)):
                self._categories[name] = Category(name, corpus=self)
        if debug.VERBOSE: print "%d categories found." % len(self._categories)

        # Read files
        for name, c in self._categories.iteritems():
            if debug.VERBOSE: print "Reading the files in %s" % name
            for f in listdir(join(root_path, name)):
                path = join(root_path, name, f)
                if isfile(path):
                    c._articles.append(Article(read_file(path), category=c, path=path))

        return self


    def update(self):
        self.scan()
        categories = self._categories

        # compute DF of category
        for name, category in categories.iteritems():
            if debug.VERBOSE: print "Compute DF of category %s" % name
            category.update_df()

        # update corpus
        self.update_size()
        self.update_df()

        for name, category in categories.iteritems():
            # compute TFIDF of articles
            if debug.VERBOSE: print "Compute TFIDF of articles in %s" % name
            for article in category._articles:
                article.update_tfidf()

        for name, category in categories.iteritems():
            # compute TFIDF of categories
            if debug.VERBOSE: print "Compute TFIDF of category %s" % name
            category.update_tfidf()

        return self




def read_file(filename):
    try:
        infile = open(filename, 'r')
        instr = infile.read()
    except:
        SystemExit('[ERROR] Read the %s!' % filename)
    finally:
        infile.close

    return instr
