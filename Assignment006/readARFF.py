#!/usr/bin/env python

import cPickle as pickle
import sys, string, random

### read in data from an ARFF file and return the following data structures:
### A dict that maps an attribute index to a dictionary mapping attribute names to either:
###    - possible values
###    - the string 'string'
###    - the string 'numeric'
### A list containing all data instances, with each instance stored as a tuple.
def readArff(filehandle) :
    attributes = {}
    data = []
    relation = ""
    ### remove all commented and blank lines.
    lines = [line for line in filehandle.readlines() if not line.startswith('%') and len(line) > 1]
    ### get all attribute lines
    attribLines = [line for line in lines if line.startswith('@attribute')]
    #this assumes the target class attribute is listed last in the ARFF file!!
    for index in range(len(attribLines)) :
        line = attribLines[index]
        chunks = [chunk.strip() for chunk in line.split(' ',2)]
        if chunks[2].startswith('{') : ### this is a nominal attribute
            attributes[index] = {chunks[1] : [item.strip() for item in chunks[2].strip('\n{} ').split(',')]}
        else : ## this is string or numeric
            attributes[index]= {chunks[1] : chunks[2]}

    # Take the clasify field specially
    index = len(attribLines)-1  # last field
    classify_attr = attributes[index]
    del attributes[index]

    ### data will be lines that don't begin with a '@'
    dataLines = [line.strip() for line in lines if not line.startswith('@')]
    for line in dataLines :
        data.append(map(string.strip, line.split(',')))
    return (attributes, data, classify_attr)



### Compute ZeroR - that is, the most common data classification without
### examining any of the attributes. Return the most comon classification.
def computeZeroR(attributes, data) :
    classes = [d[-1] for d in data]
    return max([(classes.count(key), key) for key in set(classes)])[1]


### takes as input the dictionary of attributes and returns a list of
### the attributes (only, no values) in the correct order.
def getAttrList(attrs) :
    l = [(k,attrs[k].keys()[0]) for k in attrs]
    l.sort()
    return [x[1] for x in l]




### Usage: readARFF {--pfile=outfile} infile
### If --pfile=outfile, pickle and store the results in outfile. Otherwise,
### print them to standard out. Also call computeZeroR and
### print out the results.
if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        print "Usage: readARFF {--pfile=outfile} infile"
        sys.exit(-1)
    fname = sys.argv[-1]
    (attrs, data, classify_attr) = readArff(open(fname))
    domain = classify_attr.values()[0]
    random.seed()

    print ('=' + fname).ljust(25,'=')
    for time in range(0,5):
        print " -%d time-" % (time+1)
        random.shuffle(data)
        sp = int(len(data)*4/5)
        train_data = data[:sp]
        test_data = data[sp+1:]
        zeroR = computeZeroR(attrs, train_data)
        print "  Most common classification is: ", zeroR

        # noise
        noise = 0
        for d in train_data:
            if zeroR != d[-1]: noise += 1
        print "  noise:     %d/%d=%.2f%%" % (noise, len(train_data), float(noise*100)/len(train_data))

        tp = 0
        for d in test_data:
            if zeroR == d[-1]: tp += 1
        total = len(test_data)
        fp = total-tp
        print "  precision: %d/%d=%.2f%%" % (tp, total, float(tp*100)/total)
        print "  recall:    %d/%d=%.2f%%" % (tp, tp, float(100))
        print "  accuracy:  %d/%d=%.2f%%" % (tp, total, float(tp*100)/total)
