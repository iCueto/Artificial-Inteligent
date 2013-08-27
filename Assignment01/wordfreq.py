#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cPickle as pickle
import os,sys
import re
# import time,datetime
# import heapq
# import urllib

### word frequencies:

### function that takes as input a string and, optionally,
### a dictionary, and returns the dictionary populated with word frequencies.
### provide options to strip punctuation and convert to lowercase.
##

### instr is the input string
### wf is an optional dictionary. This can be used to count over
### multiple files. If it is present, add counts to this.
### stripPunc and toLower indicate whether to strip punctuation and
### convert to lower case.

def strip(target_string, exclusive_chars=None):
    # while (len(target_string)>0) and (target_string[0] in exclusive_dict): target_string = target_string[1:]
    # while (len(target_string)>0) and (target_string[-1] in exclusive_dict): target_string = target_string[:-1]
    return target_string.lstrip(exclusive_chars).rstrip(exclusive_chars)

# punctuations = {'’','\'',',','"','[',']','(',')','{','}','⟨','⟩',':','،','、','‒','…','.','!','‐','-','?','‘','’','“','”',';','/','⁄','*','&'}
punc_chars = '’\',"[](){}⟨⟩:،、‒….!‐-?‘’“”;/⁄*&'

def wordfreq(instr, wf=None, stripPunc=True, toLower=True) :
    if not wf: wf = {}
    if toLower: instr = instr.lower()

    for key in instr.split():
        if stripPunc: key = strip(key, punc_chars)
        if key == '': continue
        if key in wf:
            wf[key] += 1
        else:
            wf[key] = 1
    return wf

### Usage: wordfreq {--nostrip --noConvert --pfile=outfile} file
### if --nostrip, don't strip punctuation
### if --noConvert, don't convert everything to lower case
### if --pfile=outfile, pickle the resulting dictionary and store it in outfile.
### otherwise, print it to standard out.

if __name__ == '__main__' :
    description = """Word Frequencies:
    function that takes as input a string and, optionally,
    a dictionary, and returns the dictionary populated with word frequencies.
    provide options to strip punctuation and convert to lowercase.
    Ranmocy Sheng, Copyright 2013, GPL
    """
    usage = """Usage: wordfreq {--nostrip --noConvert --pfile=outfile} file
    if --nostrip, don't strip punctuation
    if --noConvert, don't convert everything to lower case
    if --pfile=outfile, pickle the resulting dictionary and store it in outfile.
    otherwise, print it to standard out.
    """

    source_strings = []
    stripPunc = True
    toLower = True
    outfile = None

    for arg in sys.argv:
        if arg == '--nostrip':
            stripPunc = False
        elif arg == '--noConvert':
            toLower = False
        elif arg[0:7] == '--pfile':
            outfile = arg[8:]
        elif os.path.isfile(arg):
            if arg != sys.argv[0]: source_strings.append(open(arg).read())
        else:
            print "Unkown '%s'" % arg
            print description
            print usage
            sys.exit(1)

    if outfile:
        try:
           wf = pickle.load(open(outfile, "rb"))
        except IOError:
            wf = {}
    else:
        wf = {}

    for instr in source_strings:
        wf = wordfreq(instr, wf, stripPunc, toLower)

    if outfile:
        pickle.dump(wf, open(outfile, "wb"))
    else:
        print wf
