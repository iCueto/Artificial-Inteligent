class Cluster(object):

    def __init__(self, name, children=None):
        self._name = name
        self._tfidf = {}
        self._children = children
        if children: self.update_tfidf()


    def update_tfidf(self):
        for child in self._children:
            for word, freq in child._tfidf.iteritems():
                if word in self._tfidf:
                    self._tfidf[word] += freq
                else:
                    self._tfidf[word] = freq
        return self


    def show(self, total_width=100, fill=' '):
        output = StringIO()
        last_row = -1
        for i, n in enumerate(self):
            if i:
                row = int(math.floor(math.log(i+1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2**row
            col_width = int(math.floor((total_width * 1.0) / columns))
            output.write(str(n).center(col_width, fill))
            last_row = row
        print output.getvalue()
        return
