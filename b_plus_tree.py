'''
A B+ tree internal node (a.k.a. index node) except root should have number of children in range [order/2, order]
Correspondingly, each node should have [(order-1)/2, order-1] keys, but only leaf nodes contain all keys.
Also, in a B+ tree, all leaf nodes form a (double) linked list. 
'''
ORDER = 4
# right-biased median here, e.g., in [1, 2, 3, 4], 3 (with index 2) will be choosed as median
# if order is even, no bias is needed.
MEDIAN_INDEX = (ORDER-1) // 2 + 1

class TreeNode:

    def __init__(self, keys, children, isRoot=False, 
                 isLeaf=False, nextLeaf=None, prevLeaf=None,
                 parent=None):
        
        keys.sort()
        self.key = keys 
        self.children = children
        self.isLeaf = isLeaf
        self.isRoot = isRoot
        self.nextLeaf = nextLeaf
        self.prevLeaf = prevLeaf
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
        self.children.sort(key=lambda child: child.key[0])
    
    def isFull(self):
        if len(self.key) > ORDER-1:
            return True
        else:
            return False


class BPTree:

    def __init__(self):

        self.root = TreeNode(keys=[], children=[], isRoot=True, isLeaf=True)

    def insert(self, key):
        
        node = self.root
    
        # find the proper leaf to insert
        while not node.isLeaf:
            for i in range(len(node.key)):
                # the last key is still smaller, go to the last child
                if key < node.key[i]:
                    node = node.children[i]
                    break
                elif i == len(node.key) - 1 and key >= node.key[i]:
                    node = node.children[i+1]
                    break  
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
            leftNode = TreeNode(children=[], isLeaf=True, keys=leftKeys)
            rightNode = TreeNode(children=[], isLeaf=True, keys=rightKeys)
            leftNode.nextLeaf = rightNode
            rightNode.nextLeaf = node.nextLeaf
            leftNode.prevLeaf = node.prevLeaf
            rightNode.prevLeaf = leftNode
            if leftNode.prevLeaf != None:
                leftNode.prevLeaf.nextLeaf = leftNode
            if rightNode.nextLeaf != None:
                rightNode.nextLeaf.prevLeaf = rightNode
            # no parent, i.e., it's root
            if node.parent == None:
                parentNode = TreeNode(isRoot=True, keys=[node.key[MEDIAN_INDEX]], children=[])
                parentNode.addChild(rightNode)
                parentNode.addChild(leftNode)
                leftNode.parent = parentNode
                rightNode.parent = parentNode
                self.root = parentNode
            # parent exists
            else:
                parentNode = node.parent
                parentNode.children.remove(node)
                parentNode.addChild(rightNode)
                parentNode.addChild(leftNode)
                leftNode.parent = parentNode
                rightNode.parent = parentNode
                # split parent also if it's full
                if not parentNode.addKey(node.key[MEDIAN_INDEX]):
                    self.split(parentNode)
        # root but not leaf  
        elif node.isRoot:
            # Note: the midian will be lifted up
            upperKeys = [node.key[MEDIAN_INDEX]]

            leftKeys = node.key[0:MEDIAN_INDEX]
            rightKeys = node.key[(MEDIAN_INDEX+1):]
            leftChildren = node.children[0:(MEDIAN_INDEX+1)]
            rightChildren = node.children[(MEDIAN_INDEX+1):]

            leftNode = TreeNode(children=leftChildren, keys=leftKeys)
            rightNode = TreeNode(children=rightChildren, keys=rightKeys)
            
            # reset parents for their children
            for child in leftNode.children:
                child.parent = leftNode
            for child in rightNode.children:
                child.parent = rightNode

            # new root
            upperNode = TreeNode(isRoot=True, children=[], keys=upperKeys)
            upperNode.addChild(leftNode)
            upperNode.addChild(rightNode)

            leftNode.parent = upperNode
            rightNode.parent = upperNode

            self.root = upperNode
        # index nodes, not root
        else:
            parentNode = node.parent
            parentNode.children.remove(node)

            # Note: the midian will be lifted up
            leftKeys = node.key[0:MEDIAN_INDEX]
            rightKeys = node.key[(MEDIAN_INDEX+1):]
            leftChildren = node.children[0:(MEDIAN_INDEX+1)]
            rightChildren = node.children[(MEDIAN_INDEX+1):]

            leftNode = TreeNode(children=leftChildren, keys=leftKeys)
            rightNode = TreeNode(children=rightChildren, keys=rightKeys)

            # reset parents for their children
            for child in leftNode.children:
                child.parent = leftNode
            for child in rightNode.children:
                child.parent = rightNode
            
            parentNode.addChild(rightNode)
            parentNode.addChild(leftNode)

            leftNode.parent = parentNode
            rightNode.parent = parentNode

            if not parentNode.addKey(node.key[MEDIAN_INDEX]):
                self.split(parentNode)

    def search(self, key):

        node = self.root

        # find the proper leaf
        while not node.isLeaf:
            for i in range(len(node.key)):
                if key < node.key[i]:
                    node = node.children[i]
                    break
                # the last key is still smaller, go to the last child
                elif i == len(node.key) - 1 and key >= node.key[i]:
                    node = node.children[i+1]
                    break  
                elif key >= node.key[i]:
                    continue
        
        for k in node.key:
            if key == k:
                return True

        return False

    def prefixSearch(self, prefix):

        node = self.root

        # find the proper leaf
        while not node.isLeaf:
            for i in range(len(node.key)):
                if prefix < node.key[i]:
                    node = node.children[i]
                    break
                # the last key is still smaller, go to the last child
                elif i == len(node.key) - 1 and prefix >= node.key[i]:
                    node = node.children[i+1]
                    break  
                elif prefix >= node.key[i]:
                    continue

        if prefix < node.key[-1] or prefix in node.key:
            pass
        elif prefix > node.key[-1] and node.nextLeaf != None:
            node = node.nextLeaf
        else:
            return None

        result = []
        NextLeafNeeded = False

        prefix_next = nextWord(prefix)

        # first leaf to check, so k might be smaller than prefix
        for k in node.key:
            if k >= prefix and k < prefix_next:
                result.append(k)
                NextLeafNeeded = True
            elif k < prefix:
                continue
            else:
                NextLeafNeeded = False
                break

        # all vals in leaf is small
        if (not NextLeafNeeded) and len(result) == 0:
            return None
        # noly in this leaf
        elif not NextLeafNeeded:
            return result

        while NextLeafNeeded and node.nextLeaf != None:
            # go to next leaf
            node = node.nextLeaf

            for k in node.key:
                # it must be larger than prefix now
                if k < prefix_next:
                    result.append(k)
                    NextLeafNeeded = True
                else:
                    NextLeafNeeded = False
                    break

        return result


    def noEndLimitQuery(self, start):
        node = self.root
        # find the proper leaf
        while not node.isLeaf:
            for i in range(len(node.key)):
                if start < node.key[i]:
                    node = node.children[i]
                    break
                # the last key is still smaller, go to the last child
                elif i == len(node.key) - 1 and start >= node.key[i]:
                    node = node.children[i+1]
                    break
                elif start >= node.key[i]:
                    continue

        if start < node.key[-1] or start in node.key:
            pass
        elif start > node.key[-1] and node.nextLeaf != None:
            node = node.nextLeaf
        else:
            return None

        result = []

        # first leaf to check, so k might be smaller than start
        for k in node.key:
            if k >= start:
                result.append(k)
            elif k < start:
                continue

        # all vals in leaf is small
        if len(result) == 0:
            return None

        while node.nextLeaf != None:
            # go to next leaf
            node = node.nextLeaf

            for k in node.key:
                # it must be larger than start now
                result.append(k)

        return result

    def rangeQuery(self, start, end):
        #TODO:
        if start >= end and end != '':
            print("start should be smaller than end if end is not ''!\n")
            return None
        
        # fetch all or from start to the last one
        # prefix with no limit
        if end == '':
            return self.noEndLimitQuery(start)

        # now here is the general case [start, end]. 
        # note that start can be "" because it must be the smallest word
        # in fact, in this case, range query is just a pseudo prefix search
        # with constraint 'end' rather than nextWord(prefix) 
        
        node = self.root

        # find the proper leaf
        while not node.isLeaf:
            for i in range(len(node.key)):
                if start < node.key[i]:
                    node = node.children[i]
                    break
                # the last key is still smaller, go to the last child
                elif i == len(node.key) - 1 and start >= node.key[i]:
                    node = node.children[i+1]
                    break
                elif start >= node.key[i]:
                    continue

        if start < node.key[-1] or start in node.key:
            pass
        elif start > node.key[-1] and node.nextLeaf != None:
            node = node.nextLeaf
        else:
            return None

        result = []
        NextLeafNeeded = False

        # first leaf to check, so k might be smaller than start
        for k in node.key:
            if k >= start and k < end:
                result.append(k)
                NextLeafNeeded = True
            elif k < start:
                continue
            else:
                NextLeafNeeded = False
                break

        # all vals in leaf is small
        if (not NextLeafNeeded) and len(result) == 0:
            return None
        # noly in this leaf
        elif not NextLeafNeeded:
            return result

        while NextLeafNeeded and node.nextLeaf != None:
            # go to next leaf
            node = node.nextLeaf

            for k in node.key:
                # it must be larger than start now
                if k < end:
                    result.append(k)
                    NextLeafNeeded = True
                else:
                    NextLeafNeeded = False
                    break

        return result

    # a preorder print
    def printTree(self):
        node = self.root
        printNode(node)


def createBPTree(valList):

    tree = BPTree()
    for val in valList:
        tree.insert(val)
    
    return tree


def printNode(node):
    parent = node.parent
    if parent != None:
        parent = id(node.parent)
    
    nextLeaf = node.nextLeaf
    if nextLeaf != None:
        nextLeaf = id(node.nextLeaf)

    prevLeaf = node.prevLeaf
    if prevLeaf != None:
        prevLeaf = id(node.prevLeaf)

    print("node id:{}, keys:{}, parent:{},\n children:{},\n isLeaf:{}, isRoot:{}, nextLeaf:{}, prevLeaf: {}".format(
        id(node), node.key, parent,
        [id(child) for child in node.children],
        node.isLeaf, node.isRoot, nextLeaf, prevLeaf))

    print("------------------------------------------------")

    for child in node.children:
        printNode(child)


def nextWord(s):

    # If string is empty.
    if (s == " " or s == ""):
        return "a"

    # Find first character from right
    # which is not z.
    i = len(s) - 1
    while (s[i] == 'z' and i >= 0):
        i -= 1

    # If all characters are 'z', append
    # an 'a' at the end.
    if (i == -1):
        s = s + 'a'

    # If there are some non-z characters
    else:
        s = list(s)
        s[i] = chr(ord(s[i]) + 1)
        s = "".join(s)

    return s
