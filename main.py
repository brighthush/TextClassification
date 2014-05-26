# coding: GBK
import KNNPredict
import Training
import configuration


if __name__ == '__main__':
    testFileVectorFile = open('E:\\TextClassificationData\\test_content.txt', 'w')
    testFileVector = None
    testFileVector = KNNPredict.getDocVector(KNNPredict.test_files_to_words, Training.featureVector)
    
    result, prediction = KNNPredict.KNN(KNNPredict.training_doc_vector, testFileVector, configuration.top_k_number)
    accuracy = KNNPredict.get_accuracy(prediction)
    testFileVectorFile.write('accuracy:%.6lf'%(accuracy)+'\n')
    for doc in result:
        testFileVectorFile.write(doc.encode('gbk')+' '+prediction[doc].encode('gbk')+'\n')
        vector = result[doc]
        for neighbor in vector:
            testFileVectorFile.write('    '+neighbor[0].encode('gbk')+'\n')
            testFileVectorFile.write('    '+str(neighbor[1])+'\n')
    testFileVectorFile.close()