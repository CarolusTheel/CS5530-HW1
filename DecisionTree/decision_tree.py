from math import log2 as log

class decisionTree:
    data = []
    MCV = None  #most common value in tree
    isLeaf = False

    usedSplit = []

    next = {}

    # lower output is prefered in gainFunction, and inf is given for any that can't be chosen (no partition)
    gainFunction = None
    bestHeuristicIdx = None  #what this node returns from gain function
    
    
    def __init__(self, data):
        self.data = data
        outputs = [e[-1] for e in data]
        self.MCV = max(set(outputs), key = outputs.count)
        for i in data[0:-1]:
            self.usedSplit.append(False)

    def split(self, maxDepth):
        if maxDepth == 0:
            self.isLeaf = True

        h = self.gainFunction(self.data)

        for i in range(len(self.usedSplit)):
            if not self.usedSplit[i] and h[i] != float('inf'):
                self.bestHeuristicIdx = i
                break

        if self.bestHeuristicIdx == None:
            self.isLeaf = True
            return

        for i in range(len(self.usedSplit[i:])):
            if h[i] < h[self.bestHeuristicIdx]:
                self.bestHeuristicIdx = i
        
        self.usedSplit[self.bestHeuristicIdx] = True

        nextNodesData = {}

        for entry in data:
            if entry[self.bestHeuristicIdx] in nextNodesData.keys():
                nextNodesData[entry[self.bestHeuristicIdx]].append(entry)
            else:
                nextNodesData[entry[self.bestHeuristicIdx]] = [entry]
                  
        for k in nextNodesData.keys():
            self.next[k] = decisionTree(nextNodesData[k])
            self.next[k].usedSplit = self.usedSplit

        for k in self.next.keys():
            self.next[k].split(maxDepth-1)
        

    def print(self):
        print(self.__printNode(self, 0))



    def __printNode(self, node, tabs):
        s = ''
        for i in range(tabs):
            s += '  '
        s += str(node.bestHeuristicIdx)
        
        for k in node.next.keys():
            __printNode(node.next[k], tabs+1)

        return s


        
        
        


data = [
    [0,0,1,0,0],
    [0,0,1,1,1],
    [1,0,0,1,1]
]

print()

# CSV = 'train.csv'
# with open(CSV, 'r') as f:
#     for line in f:
#         data.append(line.strip().split(','))

root = decisionTree(data)

def majorityError(data):
    out = []
    for i in range(len(data[0])-1):
        subsets = {}

        for e in data:
            
            if not (e[i] in subsets.keys()):
                subsets[e[i]] = [0, 0]
            subsets[e[i]][e[-1]] += 1
        
        weightedME = 0

        for k in subsets.keys():
            weightedME += min(subsets[k]) / len(data)
        
        out.append(weightedME)

    return out

def infomationGain(data):
    return [0]

def giniIndex(data):
    return [0]

root.gainFunction = majorityError

root.split(1)
root.print()