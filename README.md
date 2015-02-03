TextClassification
==================

@Author: Bright Hush    
@Email: brighthush at sina dot com

# English README


## Project Introduction
This is a python project for Chinese Text Classification. I finished this project as a homework of course 
Natural Language Understanding. 

In this experiment, I use the Sougou-Text-Classification open corpus.
I used TF/IDF and Information Gain as feature extraction algorithm. As I'm lazy, I only implemented
two simple classification algorithm, they are K-Nearest-Neighbour and Naive Bayes Classification.

When extracting feature of text, We always need to segment sentences into words. I use Jieba to do word segmentation.
You can also get this module from [github](https://github.com/fxsjy/jieba).

## Naming Convention in Code
* modeule_name, package_name, method_name, function_name, instance_var_name, function_parameter_name, local_var_name
globa_var_name
* ClassName, ExceptionName
* Constant GLOBAL_VAR_NAME
* internal used element name should begin with "_"
* internal used private element name should begin with "__"

## Data Structure
### Data for training and testing
These data are sotred in train_rows and test_rows. The format of each row is described 
below.
> [row_name, dict of word bag, row_label, feature_list]
> row_name
> dict of word bag: this contains word count for each word as dict in python.
> row_label : the class of this row
> feature_list : This is a list, each element is the value corresponding to each feature.
### vocabulary information
word_hash : map each word to a int value
hash_word : this is a list, which correponding to the word_hash
hw_cnt : the size of hash_word which means the number of different words
labels: this is a set, which stores the different labels in this train data



## File and Function introduction
### read_data.py

### features.py



# 中文 README
使用搜狗语料库进行文本分类实验，此实验为《自然语言理解》课程的大作业。实验过程中使用了KNN和朴素贝叶斯方法进行分类学习，
特征提取分别采用了TF-IDF和Information Gain的方法。

ReadData.py：完成从文件中读取文本的功能，并且使用jieba模块进行分词，返回{catalog:{filename:[wordlist]}}这样的结构。

FeatureFiltering.py：对ReadData模块读入的训练数据进行词频、文档频率的统计，计算每个词对应的反文档频率idf，并且按照反文档频率从大到小进行排序，输出topK=2000的词作为
表示每个文档的特征。返回feature的结构为[(word, idf value), ...]。
除了使用tf-idf作为特征向量，还是用了信息增益的办法提取特征。

Training.py：计算每一个文档对应的tf*idf向量，返回结构为{docName: tf*idf vector, ...}。
KNNPredict.py：使用KNN算法对文本类别进行预测，计算预测结果的准确率。



