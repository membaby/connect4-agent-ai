class Board:
    def __init__(self):
        self.state = 10378549747928563776 #Corresponding to 1001000000001000000001000000001000000001000000001000000001000000
        self.maxDepth = 1
        self.mapChildren = {}
        self.mapValues = {}
        self.lastState= None
        self.numberOfNodesExpanded=0