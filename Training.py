import FeatureFiltering

featureVector = FeatureFiltering.getFeatures()
docVector = {}

# calculate tf*idf value for every doc as the representation of doc vector
for catalog in FeatureFiltering.fileToWords:
    catalog = FeatureFiltering.fileToWords[catalog]
    for doc in catalog:
        wordlist = catalog[doc]
        vector = []
        for feature in featureVector:
            vector.append(wordlist.count(feature[0])*feature[1])
        docVector[doc] = vector

def getDocVector():
    global docVector
    return docVector
