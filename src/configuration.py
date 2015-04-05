# coding: GBK
'''
This is a configuration file, you can set value for these variables.
'''

# file you will to read for test phrase, -1 means you don't limit the number of 
# test files.
test_file_number = -1

#data_directory = 'E:\\ExperimentData\\TextClassification\\SogouC.mini\\Sample'
data_directory = 'D:\\ExperimentData\\TextClassification\\SogouC.reduced\\Reduced'

#the number of features you want to filtering to represent a document
feature_number = 3000

# the number of neighbours you will use to predict a document
top_k_number = 11
knn_k = 11

# the stop words file
stopwords_file = 'E:\\Github\\TextClassification\\conf\\StopWords.txt'

idf_flag = True
ig_flag = True
