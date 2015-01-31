# coding: GBK
import configuration as conf
import os
import jieba

# read stopword from stopwords.txt
def ReadStopWords(path):
    print 'begin to read sotp_words from %s' %(path)
    f = open(path, 'r')
    stop_words = set()
    for line in f.readlines():
        line = line.strip()
        line = line.decode('gbk', 'ignore')
        stop_words.add(line)
    f.close()
    print 'finished read stop_words'
    return stop_words


# read stop words from StopWords.txt
stopWords = ReadStopWords(conf.stopwords_file)
print 'finished read stopwords ...'


# read file content from file which is named fileName, 
# then using jieba to do word segmentation
def ReadFile(fileName):
    f = open(fileName, 'r')
    text = f.read()
    text = text.decode('gbk', 'ignore')
    f.close()
    
    wordlist = jieba.cut(text, cut_all=False)
    text = []
    for word in wordlist:
        if word not in stopWords:
            text.append(word)
    return text


#read all files in directory named by dirName
def ReadDir(dir_name, training=True):
    file_content = {}
    file_cnt = 0
    file_list = os.listdir(dir_name)
    for file_name in file_list:
        t = int(file_name.split('.')[0])
        if training:
            if t%10!=0:
                text = ReadFile(dir_name+'\\'+file_name)
                file_content[dir_name+'\\'+file_name] = text
        else:
            if t%10==0:
                text = ReadFile(dir_name+'\\'+file_name)
                file_content[dir_name+'\\'+file_name] = text
        file_cnt += 1
        
        if conf.test_file_number == -1:
            continue
        if file_cnt>conf.test_file_number:
            break
    return file_content


# read all catalogs in directory named path
def ReadAllCatalogs(path, training=True):
    cataloglist = os.listdir(path)
    catalog = {}
    for name in cataloglist:
        catalog[name] = ReadDir(path+'\\'+name, training)
    return catalog

word_hash = {}
hash_word = []
hw_cnt = 0
labels = set()
rows = []
# row_name, dict of word bag, row_label
def init_train_data(catalog):
    print 'init_input_data ...'
    global word_hash # word str to number int
    global hash_word # word number to word str
    global hw_cnt # number of different words
    global labels # label set
    global rows # every line contains : row_name, dict of word bag, row_label
    for cat in catalog:
        file_list = catalog[cat]
        for file_name in file_list:
            text = file_list[file_name]            
            row = []
            row.append(file_name)
            word_bag = {}
            for word in text:
                if word not in word_hash:
                    hash_word.append(word)
                    word_hash[word] = hw_cnt
                    hw_cnt += 1
                wh_value = word_hash[word]
                if wh_value not in word_bag:
                    word_bag[wh_value] = 1
                else:
                    word_bag[wh_value] += 1
            row.append(word_bag)
            row.append(cat)
            labels.add(cat)
            rows.append(row)
    return rows, word_hash, hash_word, hw_cnt, labels

def display_rows():
    global word_hash
    global hash_word
    global hw_cnt
    global rows
    for row in rows:
        row_name = row[0]
        word_bag = row[1]
        row_label = row[2]
        print '%s\t%s' %(row_name, row_label)
        local_cnt = 0        
        for word in word_bag:
            print '[%s:%d]' %(hash_word[word].encode('gbk', 'ignore'), \
              word_bag[word])
            local_cnt += 1
            if local_cnt >= 10:
                break

def init_test_data(test_data):
    rows = []
    for cat in test_data:
        file_list = test_data[cat]
        for file_name in file_list:
            row = []
            row.append(file_name)
            word_bag = {}
            for word in file_list[file_name]:
                if word in word_hash:
                    word = word_hash[word]
                    if word in word_bag:
                        word_bag[word] += 1
                    else:
                        word_bag[word] = 1
            row.append(word_bag)
            row.append(cat)
            rows.append(row)
    return rows
    
if __name__ == '__main__':
    content = ReadAllCatalogs(conf.data_directory)
    init_train_data(content)
    display_rows()
