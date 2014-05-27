# coding: GBK
import configuration
import ReadData
import math
from operator import itemgetter

fileToWords = ReadData.ReadAllCatalogs(configuration.training_data_directory)

wordFrequency = {}
wordDocFrequency = {}
wordidf = {}
doc_word_frequency = {}

# the number of documents
docCount = 0

#the default number of features is 2000
featureNum = configuration.feature_number

#get word list and sort them by their idf value, return the [(word, idf value), ...]
def wordStatistic():
    global wordFrequency
    global wordDocFrequency
    global wordidf
    global docCount
    global doc_word_frequency
    
    for catalog in fileToWords:
        catalog = fileToWords[catalog]
        docCount += len(catalog)
        for file in catalog:
            wordBag = set()
            word_frequency = {}
            for word in catalog[file]:
                if word in wordFrequency:
                    wordFrequency[word] += 1
                else:
                    wordFrequency[word] = 1
                
                if word not in wordBag:
                    wordBag.add(word)
                    if word in wordDocFrequency:
                        wordDocFrequency[word] += 1
                    else:
                        wordDocFrequency[word] = 1
                    word_frequency[word] = 1
                else:
                    word_frequency[word] += 1
            doc_word_frequency[file] = word_frequency

    for word in wordFrequency:
        wordidf[word] = math.log(float(docCount)/float(wordDocFrequency[word]), 2)
    wordidf = sorted(wordidf.items(), key=itemgetter(1), reverse=True)
    
    return wordidf

def cal_IG(a, b, c, d, catalog_number):
    all = float(a + b + c +d)
    p_c = float(a+c)/all
    p_t = float(a+b)/all
    p_tback = float(c+d)/all
    p_c_t = float(a+1)/float(a+b+catalog_number)
    p_c_tback = float(c+1)/float(c+d+catalog_number)
    
    #print p_c_t, p_c_tback
    IG = -p_c*math.log(p_c, 2.0)+ \
    p_t*p_c_t*(math.log(p_c_t, 2.0))+p_c_tback*p_c_tback*(math.log(p_c_tback, 2.0))
    
    return IG
    
def filter_feature_IG(text_content):
    catalog_word = {}
    doc_frequency = {}
    doc_number = 0
    catalog_number = len(text_content)
    for catalog in text_content:
        doclist = text_content[catalog]
        doc_number += len(doclist)
        word_frequency = {}
        for doc in doclist:
            word_bag = set()
            for word in doclist[doc]:
                if word in word_bag:
                    continue
                word_bag.add(word)
                if word in word_frequency:
                    word_frequency[word] += 1
                else:
                    word_frequency[word] = 1
                if word in doc_frequency:
                    doc_frequency[word] += 1
                else:
                    doc_frequency[word] = 1
        catalog_word[catalog] = word_frequency
    
    word_IG = {}
    for catalog in catalog_word:
        wordlist = catalog_word[catalog]
        for word in wordlist:
            a = wordlist[word]
            c = len(text_content[catalog]) - a
            b = doc_frequency[word] - a
            d = doc_number - a - b - c
            #print a, b, c, d
            IG = cal_IG(a, b, c, d, catalog_number)
            if word in word_IG:
                word_IG[word] += IG
            else:
                word_IG[word] = IG
    
    word_IG = sorted(word_IG.items(), lambda x, y:cmp(x[1], y[1]), reverse=True)
    return word_IG
    
    
def getFeatures(topK=featureNum):
    wordidf = wordStatistic()
    wordidf = dict(wordidf)
    word_IG = filter_feature_IG(fileToWords)
    feature = {}
    
    for word, ig in word_IG[0:topK]:
        feature[word] = wordidf[word]
    return feature.items()
    
if __name__ == '__main__':
    features = getFeatures(featureNum)
    content = open('E:\\TextClassificationData\\content.txt', 'w')
    wordidf = features
    for word in wordidf:
        word, idf = word[0], word[1]
        content.write(word.encode('gbk')+' '+str(wordFrequency[word])+' '+str(wordDocFrequency[word])+' '+str(idf)+'\n')

    content.close()
