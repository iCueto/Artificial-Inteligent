#!/usr/bin/env python

import argparse
import re,sys


negative_modifier = [
"won't", "wouldn't", "shan't", "shouldn't", "can't", "cannot", "couldn't", "mustn't",
"isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't", "hadn't", "doesn't", "don't", "didn't",
"not", "no", "never"
]


def read_database(filename):
    return [line.strip() for line in open(filename, 'r').readlines() if line[0] != ';']


def read_sentences(filename, pattern):
    data = []
    for line in open(filename, 'r').readlines():
        if line[0] != ';':
            res = re.search(pattern, line.strip())
            if res:
                data.append(res.group(1))
    return data


def classify(sentence, pos_db, neg_db, handle_negative=False):
    pos = 0
    neg = 0
    reverse_flag = False

    for word in sentence.split():
        word = word.strip()
        if handle_negative:
            if word in negative_modifier:
                reverse_flag = True
                continue
        if word in pos_db:
            if reverse_flag:
                neg += 1
                reverse_flag = False
            else:
                pos += 1
        if word in neg_db:
            if reverse_flag:
                pos += 1
                reverse_flag = False
            else:
                neg += 1

    if pos > neg:
        return True
    else:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Simply use:
    `python sentiment.py`

    Wanzhang Sheng, Copyright 2013, GPL
    """)
    parser.add_argument('--handle', action='store_true', help="Handle the negation words.")
    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Be verbose to debug.")
    args = parser.parse_args()
    VERBOSE = args.verbose

    print("Reading Database..."),
    positive_db = read_database("positive-words.txt")
    negative_db = read_database("negative-words.txt")

    pros_data = read_sentences("IntegratedPros.txt", '<Pros>(.*)</Pros>')
    cons_data = read_sentences("IntegratedCons.txt", '<Cons>(.*)</Cons>')
    print("Done")
    print "positive words: %d" % len(positive_db)
    print "negative words: %d" % len(negative_db)
    print "pros sentences: %d" % len(pros_data)
    print "cons sentences: %d" % len(cons_data)

    pos = 0
    neg = 0
    total = len(pros_data)
    for sentence in pros_data:
        if classify(sentence, positive_db, negative_db, args.handle):
            pos += 1
        else:
            neg += 1
    print "Pros database positive: %d/%d=%.2f" % (pos, total, float(pos*100)/total)
    print "Pros database negative: %d/%d=%.2f" % (neg, total, float(neg*100)/total)

    pos = 0
    neg = 0
    total = len(cons_data)
    for sentence in cons_data:
        if classify(sentence, positive_db, negative_db, args.handle):
            pos += 1
        else:
            neg += 1
    print "Cons database positive: %d/%d=%.2f" % (pos, total, float(pos*100)/total)
    print "Cons database negative: %d/%d=%.2f" % (neg, total, float(neg*100)/total)
