'''
A B+ tree internal node (a.k.a. index node) except root should have number of children in range [order/2, order]
Correspondingly, each node should have [(order-1)/2, order-1] keys, but only leaf nodes contain all keys.
Also, in a B+ tree, all leaf nodes form a linked list. 
'''
ORDER = 4
# right-biased median here, e.g., in [1, 2, 3, 4], 3 (with index 2) will be choosed as median
# if order is even, no bias is needed.
MEDIAN_INDEX = (ORDER-1) // 2 + 1

def childNodeCmp(node1, node2):
    if node1.key[0] < node2.key[0]:
        return -1
    elif node1.key[0] > node2.key[1]:
        return 1
    else:
        return 0

class TreeNode:

    def __init__(self, isRoot=False, isLeaf=False, 
                 keys=[], children=[], nextLeaf=None, 
                 parent=None):
        
        keys.sort()
        self.key = keys 
        self.children = children
        self.isLeaf = isLeaf
        self.isRoot = isRoot
        self.nextLeaf = nextLeaf
        self.parent = parent

    def addKey(self, key):

        self.key.append(key)
        self.key.sort()

        if self.isFull():
            return False
        else:
            return True
    
    def addChild(self, node):

        self.children.append(node)
        self.children.sort(key=childNodeCmp)
    
    def isFull(self):
        if len(self.key) > ORDER-1:
            return True
        else:
            return False


class BPTree:

    def __init__(self):

        self.root = TreeNode(isRoot=True, isLeaf=True)

    def insert(self, key):
        
        node = self.root
    
        # find the proper leaf to insert
        while not node.isLeaf:
            for i in range(len(node.key)):
                # the last key is still smaller, go to the last child
                if key < node.key[i]:
                    node = node.children[i]
                elif i == len(node.key) - 1 and key >= node.key[i]:
                    node = node.children[i+1]  
                elif key >= node.key[i]:
                    continue
        
        # add key into this leaf
        # if the leaf now is full, split
        if not node.addKey(key):
            self.split(node)
            
    def split(self, node):
        # no children
        if node.isLeaf: 
            leftKeys = node.key[0:MEDIAN_INDEX]
            rightKeys = node.key[MEDIAN_INDEX:]
            # two new leaves
            leftNode = TreeNode(isLeaf=True, keys=leftKeys)
            rightNode = TreeNode(isLeaf=True, keys=rightKeys)
            leftNode.nextLeaf = rightNode
            # no parent
            if node.isRoot:
                parentNode = TreeNode(isRoot=True, keys=[node.key[MEDIAN_INDEX]], children=[leftNode, rightNode])
                leftNode.parent = parentNode
                rightNode.parent = parentNode
                self.root = parentNode
            # parent exists
            else:
                
        else:
            pass


    def search(self, key):

        return True

    def prefixSearch(self, prefix):

        return True

    def rangeQuery(self, low, high):

        return True

    # a preorder print
    def printTree(self):
        node = self.root
        printNode(node)


def printNode(node):
    parent = node.parent
    if parent != None:
        parent = id(node.parent)
    
    nextLeaf = node.nextLeaf
    if nextLeaf != None:
        nextLeaf = id(node.nextLeaf)

    print("node id:{}, keys:{}, parent:{}, children:{}, isLeaf:{}, isRoot:{}, nextLeaf:{}".format(
        id(node), node.key, parent,
        [id(child) for child in node.children],
        node.isLeaf, node.isRoot, nextLeaf))


    for child in node.children:
        printNode(child)
