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

    N = coMat.shape[0]

    rowCnt = 0
    colCnt = 0

    for word in coMat:
        corrMatEntry = []
        colCnt = 0
        for w in coMat:
            if colCnt < rowCnt:
                corr = 0
                corrMatEntry.append(corr)
            else:
                corr = corrCalc(word, w)
                corrMatEntry.append(corr)
            colCnt += 1
        corrMat.append(corrMatEntry)
        rowCnt += 1

    corrMat = np.array(corrMat)
    
    corrMat = np.maximum(corrMat, corrMat.transpose())

    return corrMat

# calculate correlation between two word vectors
def corrCalc(vec1, vec2):

    if vec1.shape != vec2.shape:
        sys.exit("In corrCalc: inequal vector shape.")

    correlation = np.sum(vec1 * vec2) \
                  / (np.sqrt(np.sum(np.square(vec1))) 
                    * np.sqrt(np.sum(np.square(vec2))))

    return correlation    

def createThesaurusDict(wordList):

    coMat = getCoMat(wordList)
    corrMat = getCorrMat(coMat)
    # print(corrMat)

    # wordCnt-by-(wordCnt-1)
    thesarusMat = np.argsort(-corrMat, axis=1)

    return thesarusMat

def saveThesaurusDict(thesarusMat):
    np.savez_compressed('thesarus_dict', dict=thesarusMat)