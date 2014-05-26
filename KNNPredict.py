import configuration
import Training
import ReadData
import math

docVector = Training.getDocVector()
testFileToWord = ReadData.ReadAllCatalogs(configuration.test_data_directory, False)

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

def similarity(vectora, vectorb):
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
        
def get_catalog(file_name):
    word_list = file_name.split('\\')
    return word_list[-2]
        
#determine one document by its K nearest neighbour
def determine_KNN(doc, k_nearest_neighbour):
    neighbour_count = {}
    neighbour_similarity_sum = {}
    for neighbour, value in k_nearest_neighbour:
        if True:
            neighbour = get_catalog(neighbour)
            if neighbour in neighbour_count:
                neighbour_count[neighbour] += 1
                neighbour_similarity_sum[neighbour] += value
            else:
                neighbour_count[neighbour] = 1
                neighbour_similarity_sum[neighbour] = value
    catalog = None
    for neighbour in neighbour_count:
        if catalog == None:
            catalog = neighbour
        else:
            if neighbour_count[neighbour] > neighbour_count[catalog]:
                catalog = neighbour
            elif neighbour_count[neighbour] == neighbour_count[catalog] \
                and neighbour_similarity_sum[neighbour] > neighbour_similarity_sum[catalog]:
                    catalog = neighbour
                
    return catalog
        
#get a list with K documents in the formate [(fileName, similarity value),...]
def KNN(trainVector, testVector, K=11):
    result = {}
    prediction = {}
    for testDoc in testVector:
        similarityVector = {}
        for trainDoc in trainVector:
            similarityVector[trainDoc] = similarity(testVector[testDoc], trainVector[trainDoc])
        result[testDoc] = similarityVector
        similarityVector = sorted(similarityVector.items(), lambda x, y:cmp(x[1], y[1]), reverse=True)
        result[testDoc] = similarityVector[0:K]
        prediction[testDoc] = determine_KNN(testDoc, result[testDoc])
    return result, prediction

def get_accuracy(prediction):
    true_positive = 0
    for doc in prediction:
        predicted_catalog = prediction[doc]
        doc = get_catalog(doc)
        if doc == predicted_catalog:
            true_positive += 1
    return float(true_positive)/float(len(prediction))
    
if __name__ == '__main__':
    testFileVectorFile = open('E:\\TextClassificationData\\test_content.txt', 'w')
    testFileVector = None
    testFileVector = getDocVector(testFileToWord, Training.featureVector)
    
    result, prediction = KNN(docVector, testFileVector, configuration.top_k_number)
    accuracy = get_accuracy(prediction)
    testFileVectorFile.write('accuracy:%.6lf'%(accuracy)+'\n')
    for doc in result:
        testFileVectorFile.write(doc.encode('gbk')+' '+prediction[doc].encode('gbk')+'\n')
        vector = result[doc]
        for neighbor in vector:
            testFileVectorFile.write('    '+neighbor[0].encode('gbk')+'\n')
            testFileVectorFile.write('    '+str(neighbor[1])+'\n')
    testFileVectorFile.close()
