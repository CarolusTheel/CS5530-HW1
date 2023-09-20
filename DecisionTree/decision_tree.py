from math import log2 as log


class node:
    inputDomain = []

    isLeaf = False
    mostCommonVal = None

    inputs = []
    outputs = []

    nextNodes = {}
    heuristic = None
    bestSplit = None

    def __init__(self, data, heuristic):
        self.input = [entry[:-1] for entry in data]
        self.outputs = [entry[-1] for entry in data]
        self.heuristic = heuristic

    def split(self, maxDepth):
        if maxDepth < 0:
            return
        elif maxDepth == 1:
            self.isLeaf = True
            maxCount = 0
            mostCommonVal = self.outputs[0]
            for o in self.outputs:
                count = self.outputs.count(o)
                if(count > maxCount):
                    maxCount = count
                    mostCommonVal = o
        
        # run ID3 on node
        else:
            pass
        

    def printNode(self):
        print("ID: ", self.bestSplit, " --- ", len(self.nextNodes.keys()), " child nodes", sep="")
        if self.isLeaf:
            print(self.leafVal)

data = []

with open("train.csv", 'r') as f:
    for line in f:
        data.append(line.strip().split(","))



root = node(data)