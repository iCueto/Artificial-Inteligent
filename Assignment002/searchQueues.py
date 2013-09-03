
### this is a helper function that converts a string containing latitude or longitude
## represented as degrees.minutes.seconds (e.g. 37.47.44N) into a float.
def convertLatLong(str) :
    deg, minutes,seconds = str[:-1].split('.',2)
    minutes = float(minutes) + (float(seconds) / 60.0)
    deg = float(deg) + (minutes/ 60.0)
    return deg

class SearchQueue :
    def __init__(self) :
        self.q = []

    def insert(self, item) :
        pass
    def pop(self) :
        pass
    def isEmpty(self) :
        return self.q == []

### you complete this.
class BFSQueue(SearchQueue) :
    pass

### you complete this.
class DFSQueue(SearchQueue) :
    pass

### you complete this
class AStarQueue(SearchQueue) :
    pass