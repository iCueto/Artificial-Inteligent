#!/usr/bin/env python

from ir import *
import sys, random, math

print "Interactive Test Environment"
print "Can be greater than 20, then all categories are tested eventually times."
print "Wanzhang Sheng, Copyright 2013, GPL"
print ""
print "Loading the world..."
corpus = Corpus().reset().load()

while True:
    print "Please input the number of articles to test, Press Control-D to exit:"

    line = sys.stdin.readline()
    if len(line)==0: break
    try:
        size = int(line)
        if size <= 0: raise Exception
    except:
        print "Only integer > 0 is acceptable:"
        continue

    remain = size
    right = 0
    random.seed()
    while remain>0:
        for category in corpus._categories.values():
            remain -= 1
            if remain<0: break

            prefix = "\033[93m[%d/%d]" % (size-remain, size)
            article = random.sample(category._articles, 1)[0]
            res = classify(article)
            if article._category._name == res[1]._name:
                right += 1
                prefix += '\033[92m' + "[Correct]" + '\033[0m'
            else:
                prefix += '\033[91m' + "[Fail]   " + '\033[0m'
            print "%s\t%s\t=>\t%s\twith %.2f%%" % (prefix, article._path.split('/')[-2].ljust(25), res[1]._name.ljust(25), res[0]*100)

    print "Correctness is %d/%d=%.2f%%" % (right, size, (float(right*100)/size))
