from math import log2 as log


class node:
    isLeaf = False
    mostCommonOut = None

    inputs = []
    outputs = []

    nextNodes = {}

    heuristic = None
    bestSplit = None
    usedAttributes = []

    def __init__(self, data, heuristic):
        self.inputs = [entry[:-1] for entry in data]
        self.outputs = [entry[-1] for entry in data]
        self.heuristic = heuristic
        for i in self.inputs:
            self.usedAttributes.append(False)

    def split(self, maxDepth):
        maxCount = 0
        self.mostCommonOut = self.outputs[0]
        for o in self.outputs:
            count = self.outputs.count(o)
            if(count > maxCount):
                maxCount = count
                self.mostCommonOut = o

        if maxDepth < 0:
            return
        
        elif maxDepth == 0:
            self.isLeaf = True
        
        # run ID3 on node
        elif maxCount == len(self.outputs):
            self.isLeaf = True
        
        else:
            h = self.heuristic(self.inputs, self.outputs)
            self.bestSplit = 0
            for i in range(len(h)):
                if h[i] > h[self.bestSplit] and not self.usedAttributes[i]:
                    self.bestSplit = i
            self.usedAttributes[self.bestSplit] = True




    def predict(self, input):
        if self.isLeaf:
            return self.mostCommonOut
        elif input[self.bestSplit] in self.nextNodes.keys:
            return self.nextNodes[input[self.bestSplit]].predict(input)
        else:
            return self.mostCommonOut
            

        

    def printNode(self):
        print("ID: ", self.bestSplit, " --- ", len(self.nextNodes.keys()), " child nodes", sep="")
        if self.isLeaf:
            print(self.leafVal)

data = []

with open("train.csv", 'r') as f:
    for line in f:
        data.append(line.strip().split(","))



root = node(data)