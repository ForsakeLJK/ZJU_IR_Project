import numpy as np

def getCoMat(wordList):
    
    coMat = []

    for word in wordList:
        coMatEntry = []
        for w in wordList:
            coCnt = 0
            for doc in word:
                if doc in w:
                    coCnt += 1
            coMatEntry.append(coCnt)
        coMat.append(coMatEntry)

    return np.array(coMat)
