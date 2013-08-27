import cPickle as pickle

### read in data from an ARFF file and return the following data structures:
### A dict that maps an attribute index to a dictionary mapping attribute names to either:
###    - possible values
###    - the string 'string'
###    - the string 'numeric'
### A list containing all data instances, with each instance stored as a tuple.
def readArff(filehandle) :


### Compute ZeroR - that is, the most common data classification without 
### examining any of the attributes. Return the most common classification.
def computeZeroR(attributes, data) :



### Usage: readARFF {--pfile=outfile} infile
### If --pfile=outfile, pickle and store the results in outfile. Otherwise, 
### print them to standard out. Your code should also call computeZeroR and 
### print out the results.

if__name__ == '__main__' :
    
