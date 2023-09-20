from math import log2 as log


class node:
    inputDomain = []

    isLeaf = False
    leafVal = None

    inputs = []
    outputs = []

    nextNodes = {}
    heuristic = None
    bestSplit = None

    def __init__(self, data, heuristic):
        self.input = [entry[:-1] for entry in data]
        self.outputs = [entry[-1] for entry in data]
        self.heuristic = heuristic

    def split(self):
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