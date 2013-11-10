import cPickle as pickle
import sys

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
    for index in range(len(attribLines)-1) :
        line = attribLines[index]
        chunks = line.split(' ',2)
        if chunks[2].startswith('{') : ### this is a nominal attribute
            attributes[index] = {chunks[1] : [item for item in chunks[2].strip('\n{}').split(',')]}
        else : ## this is string or numeric
            attributes[index]= {chunks[1] : chunks[2]}

    ### data will be lines that don't begin with a '@'
    dataLines = [line.strip() for line in lines if not line.startswith('@')]
    for line in dataLines :
        data.append(line.split(','))
    return (attributes, data)



### Compute ZeroR - that is, the most common data classification without
### examining any of the attributes. Return the most comon classification.
def computeZeroR(attributes, data) :
    max = 0
    maxItem = ''
    classes = [item[-1] for item in data]
    vals = set(classes)
    for item in vals :
        if classes.count(item) > max :
            classes.count(item) == max
            maxItem = item
    return maxItem


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
    (attrs, data) = readArff(open(fname))
    print "Most common classification is: ", computeZeroR(attrs,data)
    if sys.argv[1].startswith("--pfile") :
        ofile = sys.argv[1].split('=')[1]
        fh = open(ofile, 'w')
        pickle.dump(attrs, fh)
        pickle.dump(data, fh)
    else :
        print "Attributes: ", attrs
        print "Data: ", data
