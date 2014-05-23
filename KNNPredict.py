import Training
import ReadData
import math

docVector = Training.getDocVector()
testFileToWord = ReadData.ReadAllCatalogs('E:\TextClassification\SogouC.mini\Sample', False)

def getDocVector(content, featureVector):
    fileVector = {}
    for catalog in content:
        catalog = content[catalog]
        for doc in catalog:
            wordlist = catalog[doc]
            vector = []
            for feature in featureVector:
                vector.append(wordlist.count(feature[0])*feature[1])
            fileVector[doc] = vector
    return fileVector

def similarity(vectora, vectorb) :
    ans = 0
    a = 0
    b = 0
    for i in xrange(len(vectora)):
        ans += vectora[i]*vectorb[i]
        a += vectora[i]**2
        b += vectorb[i]**2
    if a*b == 0:
        return 0
    else:
        ans /= math.sqrt(a*b)
        return ans

def KNN(trainVector, testVector, K=11):
    result = {}
    for testDoc in testVector:
        similarityVector = {}
        for trainDoc in trainVector:
            similarityVector[trainDoc] = similarity(testVector[testDoc], trainVector[trainDoc])
        result[testDoc] = similarityVector
        similarityVector = sorted(similarityVector.items(), lambda x, y:cmp(x[1], y[1]), reverse=True)
        result[testDoc] = similarityVector[0:K]
    return result
    
if __name__ == '__main__':
    testFileVectorFile = open('E:\\TextClassification\\test_content.txt', 'w')
    testFileVector = None
    testFileVector = getDocVector(testFileToWord, Training.featureVector)
    
    result = KNN(docVector, testFileVector)
    for doc in result:
        testFileVectorFile.write(doc.encode('gbk')+'\n')
        vector = result[doc]
        for neighbor in vector:
            testFileVectorFile.write('    '+neighbor[0].encode('gbk')+'\n')
            testFileVectorFile.write('    '+str(neighbor[1])+'\n')
    testFileVectorFile.close()
