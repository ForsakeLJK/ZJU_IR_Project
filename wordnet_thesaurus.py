from nltk.corpus import wordnet


def get_synonyms(query, n=5):
    '''
    if n = None, returen all synonyms in wordnet
    '''

    query = query.replace('and', '')
    query = query.replace('or','')
    query = query.replace('not','')
    query = query.replace('(','')
    query = query.replace(')','')
    query = query.split(' ')
    
    Flag = True

    if n:
        n += 1

    while Flag:    
        for i in query:
            if i == '':
                query.remove(i)
        Flag = False
        for i in query:
            if i == '':
                Flag = True
    
    result = []

    for i in query:
        result.append(getThesaurus(i, n))

    return result

def getThesaurus(word, n=5):
    thesaurus = []
    
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name() in thesaurus:
                pass
            elif "_" in list(l.name()):
                pass
            elif "-" in list(l.name()):
                pass
            else:
                thesaurus.append(l.name())

    if n == None:
        return thesaurus

    if len(thesaurus) > (n+1):
        thesaurus = thesaurus[1:n]
    elif len(thesaurus) <= 1:
        thesaurus = []
    else:
        thesaurus = thesaurus[1:]

    return thesaurus
