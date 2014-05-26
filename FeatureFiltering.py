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
    

def getFeatures(topK=featureNum):
    wordidf = wordStatistic()
    return wordidf[0:topK]
    
if __name__ == '__main__':
    features = getFeatures(featureNum)
    content = open('E:\\TextClassification\\Data\\content.txt', 'w')
    wordidf = features
    for word in wordidf:
        word, idf = word[0], word[1]
        content.write(word.encode('gbk')+' '+str(wordFrequency[word])+' '+str(wordDocFrequency[word])+' '+str(idf)+'\n')

    content.close()
