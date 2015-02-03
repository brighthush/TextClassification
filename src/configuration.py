# coding: GBK
'''
This is a configuration file, you can set value for these variables.
'''

#file you will to read, you can change it to test
test_file_number = 300

#data_directory = 'E:\\ExperimentData\\TextClassification\\SogouC.mini\\Sample'
data_directory = 'E:\\ExperimentData\\TextClassification\\SogouC.reduced\\Reduced'

# training data directory
training_data_directory = data_directory

# test data directory
test_data_directory = data_directory

#the number of features you want to filtering to represent a document
feature_number = 3000

# the number of neighbours you will use to predict a document
top_k_number = 11
knn_k = 11

# the stop words file
stopwords_file = 'E:\\Github\\TextClassification\\conf\\StopWords.txt'

idf_flag = True
ig_flag = True
