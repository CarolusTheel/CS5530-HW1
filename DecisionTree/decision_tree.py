from math import log2 as log

class decisionTree:
    data = []
    MCV = None  #most common value in tree
    isLeaf = False

    usedSplit = []

    next = {}

    gainFunction = None
    nodeHeuristicIdx = None  #what this node returns from gain function
    
    
    def __init__(self, data):
        self.data = data
        for i in data[0:-1]:
            self.usedSplit.append(False)

    def split(self, maxDepth):
        pass



data = [
    [0,0,1,0,0],
    [0,1,0,0,0],
    [0,0,1,1,1],
    [1,0,0,1,1],
    [0,1,1,0,0],
    [1,1,0,0,0],
    [0,1,0,1,0]
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
        subset = [[data[i], data[-1]] for x in data if data[i] == 1]
        y,n = 0
        for e in subset:
            if e[1]:
                y+=1
            else:
                n+=1
        sum = y+n
        y /= sum
        n /= sum

        ME = min(y,n)
        ME *= len(subset)/len(data)
        out.append(ME)

    return out

def infomationGain(data):
    return 0

def giniIndex(data):
    return 0

root.gainFunction = infomationGain

root.split(6)