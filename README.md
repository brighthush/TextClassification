TextClassification
==================

使用搜狗语料库进行文本分类实验，此实验为《自然语言理解》课程的大作业。实验过程中使用了KNN和朴素贝叶斯方法进行分类学习，
特征提取分别采用了TF-IDF和Information Gain的方法。

ReadData.py：完成从文件中读取文本的功能，并且使用jieba模块进行分词，返回{catalog:{filename:[wordlist]}}这样的结构。

FeatureFiltering.py：对ReadData模块读入的训练数据进行词频、文档频率的统计，计算每个词对应的反文档频率idf，并且按照反文档频率从大到小进行排序，输出topK=2000的词作为
表示每个文档的特征。返回feature的结构为[(word, idf value), ...]。
除了使用tf-idf作为特征向量，还是用了信息增益的办法提取特征。

Training.py：计算每一个文档对应的tf*idf向量，返回结构为{docName: tf*idf vector, ...}。
KNNPredict.py：使用KNN算法对文本类别进行预测，计算预测结果的准确率。


author: BrightHush
email:brighthush at sina dot com
