#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cPickle as pickle
import argparse
import string

### read in data from an ARFF file and return the following data structures:
### A dict that maps an attribute index to a dictionary mapping attribute names to either:
###    - possible values
###    - the string 'string'
###    - the string 'numeric'
### A list containing all data instances, with each instance stored as a tuple.
def readArff(filehandle):
    index = 0
    attrs = {}
    data = []

    # Attributes
    for line in filehandle:
        line = line.strip("\n\r ")
        if len(line) == 0: continue
        if line[0] == '%' : continue
        if line[:10].lower() == '@attribute':
            index += 1
            parts = line.split(' ')
            name,attr_str = parts[1],string.join(parts[2:],'')
            attr_list = attr_str[1:-1].split(",")
            attrs[index] = {name: attr_list}
        if line[:9].lower()  == '@relation' : continue #TODO if I use class may record name somewhere.
        if line[:5].lower()  == '@data' : break

    # Data
    for line in filehandle:
        line = line.strip("\n\r ")
        if len(line) == 0: continue
        if line[0] == '%': continue
        data.append(tuple(line.split(',')))

    return attrs, data

### Compute ZeroR - that is, the most common data classification without
### examining any of the attributes. Return the most common classification.
def computeZeroR(attributes, data) :
    counter = {}
    for datum in data:
        choice = datum[-1]
        if choice in counter:
            counter[choice] += 1
        else:
            counter[choice] = 1
    max_count = 0
    ans = None
    for choice,count in counter.iteritems():
        if max_count < count:
            max_count = count
            ans = choice
    return ans


### Usage: readARFF {--pfile=outfile} infile
### If --pfile=outfile, pickle and store the results in outfile. Otherwise,
### print them to standard out. Your code should also call computeZeroR and
### print out the results.

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
    """read in data from an ARFF file and return the following data structures:
    A dict that maps an attribute index to a dictionary mapping attribute names to either:
    - possible values
    - the string 'string'
    - the string 'numeric'
    A list containing all data instances, with each instance stored as a tuple.
    """
    )
    parser.add_argument('--pfile', dest='outfile', type=argparse.FileType('w'),
                        help="""If --pfile=outfile, pickle and store the results in outfile. Otherwise,
                        print them to standard out. Your code should also call computeZeroR and
                        print out the results."""
                        )
    parser.add_argument('infile', type=file, help='The intput file.')

    args = parser.parse_args()

    attrs, data = readArff(args.infile)
    args.infile.close

    if args.outfile:
        pickle.dump(attrs, args.outfile)
        pickle.dump(data, args.outfile)
        args.outfile.close
    else:
        print attrs
        print data

    print computeZeroR(attrs, data)
