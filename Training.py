# coding: GBK
import FeatureFiltering

print 'began to filter features'
featureVector = FeatureFiltering.global_features
print 'finished fitering features'

# calculate tf*idf value for every doc as the representation of doc vector
def getDocVector():
    global featureVector
    docVector = {}
    
    for catalog in FeatureFiltering.fileToWords:
        catalog = FeatureFiltering.fileToWords[catalog]
        for doc in catalog:
            wordlist = catalog[doc]
            word_frequency = FeatureFiltering.doc_word_frequency[doc]
            vector = []
            for feature in featureVector:
                if feature[0] in word_frequency:
                    vector.append((float(word_frequency[feature[0]]))*feature[1])
                else:
                    vector.append(0.0)
            docVector[doc] = vector
    return docVector
