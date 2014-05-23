# coding: GBK
import ReadData
import math
from operator import itemgetter

fileToWords = ReadData.ReadAllCatalogs('E:\TextClassification\SogouC.mini\Sample')

wordFrequency = {}
wordDocFrequency = {}
wordidf = {}
docCount = 0

featureNum = 2000

def wordStatistic():
    global wordFrequency
    global wordDocFrequency
    global wordidf
    global docCount
    
    for catalog in fileToWords:
        catalog = fileToWords[catalog]
        docCount += len(catalog)
        for file in catalog:
            wordBag = set()
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

    for word in wordFrequency:
        wordidf[word] = math.log(float(docCount)/float(wordDocFrequency[word]), 2)
    wordidf = sorted(wordidf.items(), key=itemgetter(1), reverse=True)
    
    return wordidf
    

def getFeatures(topK=featureNum):
    wordidf = wordStatistic()
    return wordidf[0:topK]
    
if __name__ == '__main__':
    features = getFeatures(featureNum)
    content = open('E:\\TextClassification\\content.txt', 'w')
    wordidf = features
    for word in wordidf:
        word, idf = word[0], word[1]
        content.write(word.encode('gbk')+' '+str(wordFrequency[word])+' '+str(wordDocFrequency[word])+' '+str(idf)+'\n')

    content.close()