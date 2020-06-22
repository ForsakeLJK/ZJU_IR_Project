from thesaurus_expansion import createThesaurusDict, saveThesaurusDict
import numpy as np
# list.index() can translate words into index
# [[docIDs]]
# 5 words, 10 docs here
test = [
        [1, 3, 4, 7, 9],
        [2, 3, 5, 7, 10],
        [6, 7, 8, 9, 10],
        [3, 4, 5, 6, 7, 10],
        [2, 3, 4, 5, 8]
        ]

# test = np.array(test)

# D = np.max(np.max(test))
# N = test.shape[0]

# for i in range(N):
# 	ncols = len(test[i])
# 	for j in range(ncols):
# 		test[i][j] -= 1

# print(test)

# test_2 = np.zeros((N, D))

# print(test_2.shape)

# for i in range(N):
# 	test_2[i, test[i]] = 1

# print(test_2)
	

# test = [
#         [1, 0, 1, 1, 0, 0, 1, 0, 1, 0],
#         [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
#         [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
#         [0, 0, 1, 1, 1, 1, 1, 0, 0, 1],
#         [0, 1, 1, 1, 1, 0, 0, 1, 0, 0]
# ]

# test = np.array(test)

# print(np.dot(test_2, test_2.T))

thesaurusDict = createThesaurusDict(test)
saveThesaurusDict(thesaurusDict)

print(thesaurusDict)


# coMat:
# [[5 2 2 3 2]
#  [2 5 2 4 3]
#  [2 2 5 3 1]
#  [3 4 3 6 3]
#  [2 3 1 3 5]]

# corrMat:
# [[1.         0.81312325 0.78696406 0.87919135 0.78741229]
#  [0.81312325 1.         0.78093769 0.96025331 0.90971765]
#  [0.78696406 0.78093769 1.         0.85787148 0.63832691]
#  [0.87919135 0.96025331 0.85787148 1.         0.87691923]
#  [0.78741229 0.90971765 0.63832691 0.87691923 1.        ]]

# thesaurusDict:
# [[3 1 4 2]
#  [3 4 0 2]
#  [3 0 1 4]
#  [1 0 4 2]
#  [1 3 0 2]]

# [[0 3 1 4 2]
#  [1 3 4 0 2]
#  [2 3 0 1 4]
#  [3 1 0 4 2]
#  [4 1 3 0 2]]
