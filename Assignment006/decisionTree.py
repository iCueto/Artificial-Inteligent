#!/usr/bin/env python

import sys, math, re, itertools, argparse, random
import cPickle as pickle
import readARFF


### takes as input a list of class labels. Returns a float
### indicating the entropy in this data. Input:
###     [class1, class2, class3, ..., classn]
def entropy(results):
    ans = {key: 0 for key in results}
    for d in results: ans[d] += 1
    e = 0
    size = len(results)
    for key, freq in ans.iteritems():
        p = float(freq)/size
        e += -p*math.log(p, 2)
    return e


### Compute remainder - this is the amount of entropy left in the data after
### we split on a particular attribute. Let's assume the input data is of
### the form:
###    [(value1, class1), (value2, class2), ..., (valuen, classn)]
def remainder(data) :
    possibleValues = set([item[0] for item in data])
    r = 0.0
    for value in possibleValues :
        c = [item[0] for item in data].count(value)
        r += (float(c) / len(data) ) * entropy([item[1] for item in
                                                data if item[0] == value])
    return r


### selectAttribute: choose the index of the attribute in the current
### dataset that minimizes the remainder.
### data is in the form [[a1, a2, ..., c1], [b1,b2,...,c2], ... ]
### where the a's are attribute values and the c's are classifications.
### and attributes is a list [a1,a2,...,an] of corresponding attribute values
def selectAttribute(data, attributes) :
    #you write this
    min_rem = float('inf')
    min_index = -1
    for index, attr in attributes.iteritems():
        rem = remainder([(d[index], d[-1]) for d in data])
        if rem < min_rem:
            min_rem = rem
            min_index = index
    return min_index


def ZeroR(data):
    values = sorted([d[-1] for d in data])
    return max([key for key,freq in itertools.groupby(values)])


### a TreeNode is an object that has either:
### 1. An attribute to be tested and a set of children; one for each possible
### value of the attribute.
### 2. A value (if it is a leaf in a tree)
class TreeNode :
    def __init__(self, attribute=None, value=None, children=None, defaultValue=None) :
        self.attribute = attribute
        self.value = value
        if children:
            self.children = children
            if defaultValue == None:
                self.defaultValue = ZeroR(self.children)
            else:
                self.defaultValue = defaultValue
        else:
            self.children = []
            self.defaultValue = defaultValue

    def __repr__(self, indent='') :
        if not self.isLeaf():
            children_repr = ''
            for value, child in self.children.iteritems():
                children_repr += child.__repr__(indent=indent+'| ')
            return "%s%s:%d\n%s" % (indent, self.value, self.attribute, children_repr)
        else :
            return "%s%s\n" % (indent, self.value)

    ### a node with no children is a leaf
    def isLeaf(self) :
        return self.attribute == None


    ### return the value for the given data
    ### the input will be:
    ### data - an object to classify - [v1, v2, ..., vn]
    ### attributes - the attribute dictionary
    def classify(self, data, attributes) :
        if not self.isLeaf():
            return self.children[data[self.attribute]].classify(data, attributes)
        else:
            return self.defaultValue


### a tree is simply a data structure composed of nodes (of type TreeNode).
### The root of the tree
### is itself a node, so we don't need a separate 'Tree' class. We
### just need a function that takes in a dataset and our attribute dictionary,
### builds a tree, and returns the root node.
### makeTree is a recursive function. Our base case is that our
### dataset has entropy 0 - no further tests have to be made. There
### are two other degenerate base cases: when there is no more data to
### use, and when we have no data for a particular value. In this case
### we use either default value or majority value.
### The recursive step is to select the attribute that most increases
### the gain and split on that.


### assume: input looks like this:
### dataset: [[v1, v2, ..., vn, c1], [v1,v2, ..., c2] ... ]
### attributes: [a1,a2,...,an] }
def makeTree(data, attributes, value=None, defaultValue=None) :
    # If no more available attr to test. Or entropy is 0
    e = entropy([d[-1] for d in data])
    if (len(attributes) == 0) or (e == 0): return TreeNode(value=value, children=data)

    choice = selectAttribute(data, attributes) # Choice the best attr for test
    values = attributes[choice].values()[0]    # Candidates values for this attr
    # Group the data
    children_data = {value: [item for item in data if item[choice]==value] for value in values}
    if len(children_data)==1:
        # return a leaf if the attr tells nothing
        return TreeNode(value=value, children=data)
    else:
        remained_attrs = attributes.copy()
        del remained_attrs[choice]
        children = {}
        for child, child_data in children_data.iteritems():
            if len(child_data) == 0:
                children[child] = TreeNode(value=child, children=child_data, defaultValue=ZeroR(data))
            else:
                children[child] = makeTree(child_data, remained_attrs, value=child)
        node = TreeNode(attribute=choice, value=value, children=children)
        return node


# Return empty statistics dictionary
def init_statistics(domain):
    return {answer: {a:0 for a in domain} for answer in domain}


# precision: TP/(TP+FP)
# recall: TP/(TP+TN)
# accuracy: (TP+FN)/A
def print_test(test_data):
    TP = test_data[domain[0]][domain[0]]
    FP = test_data[domain[-1]][domain[0]]
    TN = test_data[domain[0]][domain[-1]]
    FN = test_data[domain[-1]][domain[-1]]
    total = TP+FP+TN+FN
    print "  precision: %d/%d=%.2f%%" % (TP, (TP+FP), float(TP*100)/(TP+FP))
    print "  recall:    %d/%d=%.2f%%" % (TP, (TP+TN), float(TP*100)/(TP+TN))
    print "  accuracy:  %d/%d=%.2f%%" % (TP+FN, total, float((TP+FN)*100)/total)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Simply use to test:
    `python decisionTree.py ARFF_FILE`

    Wanzhang Sheng, Copyright 2013, GPL
    """)
    parser.add_argument('arff_file', help='The source ARFF file.')
    parser.add_argument('--verbose', dest='verbose', action='store_true', help="Be verbose to debug.")
    args = parser.parse_args()
    VERBOSE = args.verbose

    (attrs, data, classify_attr) = readARFF.readArff(open(args.arff_file))
    domain = classify_attr.values()[0]
    random.seed()

    print ('=' + args.arff_file).ljust(25,'=')
    total = init_statistics(domain)
    total_noise = 0
    for time in range(0,5):
        print " -%d time-" % (time+1)
        random.shuffle(data)
        sp = int(len(data)*4/5)
        train_data = data[:sp]
        test_data = data[sp+1:]
        root = makeTree(train_data, attrs)

        # noise
        noise = 0
        for d in train_data:
            if root.classify(d, attrs) != d[-1]:
                noise += 1
        total_noise += noise
        print "  noise:     %d/%d=%.2f%%" % (noise, len(train_data), float(noise*100)/len(train_data))

        the_round = init_statistics(domain)
        for d in test_data:
            res = root.classify(d, attrs)
            the_round[d[-1]][res] += 1
            total[d[-1]][res] += 1
        print_test(the_round)

    print ' -total-'
    print "  noise:     %d/%d=%.2f%%" % (total_noise, len(train_data)*5, float(total_noise*20)/len(train_data))
    print_test(total)

    print "=End".ljust(25,'=')
