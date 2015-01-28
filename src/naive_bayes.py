# coding: GBK

import math
import FeatureFiltering
import KNNPredict

training_doc_to_word = FeatureFiltering.fileToWords
test_doc_to_word = KNNPredict.test_files_to_words
features = FeatureFiltering.global_features
catalog_p = {}
catalog_word_p = {}

def cal_catalog_word_pro(training_content, features):
    
    global catalog_p
    global catalog_word_p
    
    for catalog in training_content:
        docdict = training_content[catalog]
        
        value = float(1+len(docdict))/float(len(training_content)+FeatureFiltering.docCount)
        value = math.log(value)
        catalog_p[catalog] = value
        
        word_p = {}
        for word, value in features:
            doc_cnt = 0
            for doc in docdict:
                if word in docdict[doc]:
                    doc_cnt += 1
            word_p[word] = float(doc_cnt+1)/float(FeatureFiltering.wordDocFrequency[word]+len(training_content))
            word_p[word] = math.log(word_p[word])
        
        catalog_word_p[catalog] = word_p
    return catalog_word_p

def get_predicted_catalog(nb_prediction):

    catalog_predicted = {}
    for doc in nb_prediction:
        catalog_pro = nb_prediction[doc]
        predicted_ans = None
        for catalog in catalog_pro:
            if predicted_ans == None:
                predicted_ans = catalog
            elif catalog_pro[catalog] > catalog_pro[predicted_ans]:
                predicted_ans = catalog
        catalog_predicted[doc] = predicted_ans
    return catalog_predicted

def predict_nb(test_content, features):

    print 'begin cal_catalog_word_pro'
    cal_catalog_word_pro(training_doc_to_word, features)
    print 'finished cal_catalog_word_pro'
    
    global catalog_p
    global catalog_word_p
    
    print 'begin predicting by naive bayes'
    nb_prediction = {}
    
    for catalog in test_content:
        doclist = test_content[catalog]
        for doc in doclist:
            print 'test doc: '+doc.encode('gbk')+'\n'
            
            doc_catalog_pro = {}
            wordlist = doclist[doc]
            
            for catalog_try in catalog_p:
                likely = catalog_p[catalog_try]
                for word, value in features:
                    if word in wordlist:
                        likely += catalog_word_p[catalog_try][word]
                doc_catalog_pro[catalog_try] = likely
            
            nb_prediction[doc] = doc_catalog_pro
    
    catalog_predicted = get_predicted_catalog(nb_prediction)
    return catalog_predicted


if __name__ == '__main__':
    ans = predict_nb(test_doc_to_word, FeatureFiltering.global_features)
    print 'finished predicted by naive bayes'
    true_positive, predicted_num, accuracy = KNNPredict.get_accuracy(ans)
    file = open('E:\\TextClassificationData\\nb_content.txt', 'w')
    file.write('true_positive, predicted_num, accuracy, %d %d %6lf \n' \
    %(true_positive, predicted_num, accuracy))
    for doc in ans:
        file.write(doc.encode('gbk')+'\n')
        file.write('    '+ans[doc].encode('gbk')+'\n')
    file.close()
    