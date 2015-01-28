# coding=GBK
import KNNPredict
import Training
import configuration

def main():
    pass

if __name__ == '__main__':
    testFileVectorFile = open('E:\\Github\\TextClassification\\conf\\test_content.txt', 'w')
    testFileVector = None
    
    print 'began to get testFileVector'
    testFileVector = KNNPredict.getDocVector(KNNPredict.test_files_to_words, Training.featureVector)
    print 'finished getting testFileVector'
    
    print 'began to predicting by knn method'
    result, prediction = KNNPredict.KNN(KNNPredict.training_doc_vector, testFileVector, configuration.top_k_number)
    true_positive, predicted, accuracy = KNNPredict.get_accuracy(prediction)
    print 'finished predicting'
    
    testFileVectorFile.write('%d %d accuracy:%.6lf'%(true_positive, predicted, accuracy)+'\n')
    for doc in result:
        testFileVectorFile.write(str(doc).encode('gbk')+' '+str(prediction[doc]).encode('gbk')+'\n')
        vector = result[doc]
        for neighbor in vector:
            testFileVectorFile.write('    '+neighbor[0].encode('gbk')+'\n')
            testFileVectorFile.write('    '+str(neighbor[1])+'\n')
    testFileVectorFile.close()
