import numpy as np
import sys
from scipy import linalg
from sklearn.utils import check_array



def getCoMat(wordList):

    wordList = np.array(wordList)
    D = np.max(np.max(wordList))
    N = wordList.shape[0]

    for i in range(N):
        ncols = len(wordList[i])
        for j in range(ncols):
            wordList[i][j] -= 1

    coMat = np.zeros((N, D))

    for i in range(N):
        coMat[i, wordList[i]] = 1

    coMat = fast_dot(coMat, coMat.T)

    print("getCoMat done.")

    return coMat


def getCorrMat(coMat):

    

    

    N = coMat.shape[0]

    corrMat = np.zeros((N, N))

    rowCnt = 0
    colCnt = 0

    for word in coMat:
        # corrMatEntry = []
        colCnt = 0
        for w in coMat:
            if colCnt < rowCnt:
                corr = 0
                # corrMatEntry.append(corr)
                corrMat[rowCnt, colCnt] = corr
            else:
                corr = np.sum(word * w) \
                    / (np.linalg.norm(word) * np.linalg.norm(w))
                # corrMatEntry.append(corr)
                corrMat[rowCnt, colCnt] = corr
            colCnt += 1
        # corrMat.append(corrMatEntry)
        if rowCnt != 0 and rowCnt % 10000 == 0:
            print("10000 rows passed in getCorrMat")
        rowCnt += 1

    # corrMat = np.array(corrMat)

    corrMat = np.maximum(corrMat, corrMat.transpose())

    print("getCorrMat done.")

    return corrMat


def createThesaurusDict(wordList):

    coMat = getCoMat(wordList)
    corrMat = getCorrMat(coMat)
    # print(corrMat)

    # wordCnt-by-(wordCnt-1)
    thesarusMat = np.argsort(-corrMat, axis=1)[:, 0:10]

    return thesarusMat


def saveThesaurusDict(thesarusMat):
    np.savez_compressed('thesarus_dict', dict=thesarusMat)

def fast_dot(A, B):
    """Compute fast dot products directly calling BLAS.
    This function calls BLAS directly while warranting Fortran contiguity.
    This helps avoiding extra copies `np.dot` would have created.
    For details see section `Linear Algebra on large Arrays`:
    http://wiki.scipy.org/PerformanceTips
    Parameters
    ----------
    A, B: instance of np.ndarray
        input matrices.
    """
    if A.dtype != B.dtype:
        raise ValueError('A and B must be of the same type.')
    if A.dtype not in (np.float32, np.float64):
        raise ValueError('Data must be single or double precision float.')

    dot = linalg.get_blas_funcs('gemm', (A, B))
    A, trans_a = _impose_f_order(A)
    B, trans_b = _impose_f_order(B)
    return dot(alpha=1.0, a=A, b=B, trans_a=trans_a, trans_b=trans_b)


def _impose_f_order(X):
    """Helper Function"""
    # important to access flags instead of calling np.isfortran,
    # this catches corner cases.
    if X.flags.c_contiguous:
        return check_array(X.T, copy=False, order='F'), True
    else:
        return check_array(X, copy=False, order='F'), False
