#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cPickle as pickle
import os,sys
import re
import argparse
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
    parser = argparse.ArgumentParser(description="""Word Frequencies:
    function that takes as input a string and, optionally,
    a dictionary, and returns the dictionary populated with word frequencies.
    provide options to strip punctuation and convert to lowercase.
    Ranmocy Sheng, Copyright 2013, GPL
    """)
    parser.add_argument('source_file', type=file, help='The source file.')
    parser.add_argument('--nostrip', dest='stripPunc', action='store_false',
                       help='if --nostrip, don\'t strip punctuation')
    parser.add_argument('--noConvert', dest='toLower', action='store_false',
                       help='if --noConvert, don\'t convert everything to lower case')
    parser.add_argument('--outfile', dest='outfile',
                       help='if --pfile=outfile, pickle the resulting dictionary and store it in outfile. otherwise, print it to standard out.')

    args = parser.parse_args()

    if args.outfile:
        try:
            wf = pickle.load(open(args.outfile, 'r'))
        except:
            print 'Skip reading from the outfile, since it is not exist.'
            wf = {}
    else:
        wf = {}

    try:
        instr = args.source_file.read()
    except:
        SystemExit('[ERROR] Read the source file!')
    finally:
        args.source_file.close

    wf = wordfreq(instr, wf, args.stripPunc, args.toLower)

    if args.outfile:
        try:
            pickle.dump(wf, open(args.outfile, 'w'))
        except:
            print '[ERROR] Can not write to outfile!'
            print wf
    else:
        print wf
