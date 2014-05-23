import FeatureFiltering

featureVector = FeatureFiltering.getFeatures()
docVector = {}

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
        