from b_plus_tree import createBPTree

# lexicographical ordering

# 57 words
# wordList = ['brought', 'cat', 'coffee', 'is', 'dude', 
#             'crap', 'zoo', 'christ', 'topology', 'lexical',
#             'mother', 'emergency', 'forsake', 'google', 'halo',
#             'kangroo', 'corrupted', 'loom', 'monstrosity', 'odd',
#             'popularity', 'qualified', 'surreal', 'repository', 'vow',
#             'variety', 'similarity', 'roll', 'voila', 'oddity',
#             'unfamiliar', 'logistic', 'logic', 'witch', 'oral', 
#             'intercourse', 'horizon', 'vertical', 'symmetry', 'loss',
#             'defense', 'of', 'ancient', 'company', 'stone',
#             'glasses', 'maze', 'curiosity', 'random', 'tree', 'text',
#             'text-book', 'fear', 'afraid', 'frightened', 'novel', 'top']

wordList = ['brought', 'cat', 'coffee', 'is', 'dude',
            'crap', 'zoo', 'forsake', 'google', 'halo',
            'kangroo', 'corrupted',  'random', 'tree', 'text',
            'text-book', 'fear', 'afraid', 'frightened', 'novel', 'top']

tree = createBPTree(wordList)
# for word in wordList:
#     if not tree.search(word):
#         print("error!")
# print("search \'cook\', python result: {}, tree result: {}".format(
#     'cook' in wordList, tree.search('cook')))

tree.printTree()
# print(tree.prefixSearch('top'))
# print(tree.prefixSearch('te'))
# print(tree.prefixSearch('i'))
# print(tree.prefixSearch(' '))
# print(tree.rangeQuery('b', 'e'))
# print(tree.rangeQuery('', 'e'))
# print(tree.rangeQuery('a', 'ab'))
# print(len(tree.rangeQuery('', '')))
# print(tree.rangeQuery('', ''))
# print(len(tree.rangeQuery('cat', ''))) 
# print(tree.rangeQuery('cat', ''))
