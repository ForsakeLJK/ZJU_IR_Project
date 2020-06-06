import numpy as np
import sys

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

def getCorrMat(coMat):

    corrMat = []

    for word in coMat:
        corrMatEntry = []
        for w in coMat:
            corr = corrCalc(word, w)
            corrMatEntry.append(corr)
        corrMat.append(corrMatEntry)

    corrMat = np.array(corrMat)

    return corrMat

# calculate correlation between two word vectors
def corrCalc(vec1, vec2):

    if vec1.shape != vec2.shape:
        sys.exit("In corrCalc: unequal vec shape.")

    correlation = np.sum(vec1 * vec2) \
                  / (np.sqrt(np.sum(np.square(vec1))) 
                    * np.sqrt(np.sum(np.square(vec2))))

    return correlation    

def createThesaurusDict(wordList):

    coMat = getCoMat(wordList)
    corrMat = getCorrMat(coMat)
    # print(corrMat)

    # wordCnt-by-(wordCnt-1)
    thesarusMat = np.argsort(-corrMat, axis=1)[:, 1:]

    return thesarusMat