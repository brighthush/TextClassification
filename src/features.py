# coding=GBK
import configuration as conf
import read_data as rd
import math

hash_word = rd.hash_word

def cal_idf(input_rows):
    doc_frequence = {}
    for row in input_rows:
        word_bag = row[1]
        for word in word_bag:
            if word not in doc_frequence:
                doc_frequence[word] = 1
            else:
                doc_frequence[word] += 1
    idfs = doc_frequence.items()
    idfs.sort(lambda x, y: cmp(x[1], y[1]))
    #for i in range(10):
    #    print idfs[i][0], idfs[i][1], hash_word[idfs[i][0]]
    return idfs

# input line
# line_name, dict of word bag, label
def cal_entropy(input_rows, labels):
    label_cnt = {}
    for label in labels: # 平滑
        label_cnt[label] = 1
    label_total = len(input_rows) + len(labels)
    for row in input_rows:
        label = row[2]
        label_cnt[label] += 1
    prob = []
    for label in label_cnt:
        prob.append(float(label_cnt[label]) / float(label_total))
    entr = 0
    for p in prob:
        entr += (- p * math.log(p, 2.0))
    return entr
    
# return list of entropy for each word
def word_entropy(input_rows, words, labels):
    entrs = {}
    for word in range(len(words)):
        pos_set = []
        neg_set = []
        for row in input_rows:
            if word in row[1]:
                pos_set.append(row)
            else:
                neg_set.append(row)
        entr = cal_entropy(pos_set, labels) + cal_entropy(neg_set, labels)
        entrs[word] = entr
    entrs = entrs.items()
    entrs.sort(lambda x, y: cmp(x[1], y[1]))
    #for i in range(10):
    #   print entrs[i][0], ':', entrs[i][1], ReadData.hash_word[entrs[i][0]]
    return entrs
    
def get_features(feature_num, input_rows, words, labels):
    feature_set = set()
    idfs = cal_idf(input_rows)
    word_idf = [0] * len(input_rows)
    for idf in idfs:
        word_idf[idf[0]] = idf[1]
    if conf.idf_flag:
        for i in range(min(feature_num, len(idfs))):
            feature_set.add(idfs[i][0])
    if conf.ig_flag:
        igs = word_entropy(input_rows, words, labels)
        for i in range(min(feature_num, len(igs))):
            feature_set.add(igs[i][0])
    features = []
    features_weight = []
    for fea in feature_set:
        features.append(fea)
        features_weight.append(word_idf[fea])
    #print 'feature dimision is %d' %(len(features))
    #for fea in features:
    #    print hash_word[fea]
    return features, features_weight

def add_feature(input_rows, features):
    for row in input_rows:
        feas = []
        for fea in features:
            if fea in row[1]:
                feas.append(row[1][fea])
            else:
                feas.append(0)
        row.append(feas)
    return input_rows

def prepare_data(data_path):
    train_data = rd.read_catalogs(data_path)
    test_data = rd.read_catalogs(data_path, False)
    rows, word_hash, hash_word, hw_cnt, labels = rd.init_train_data(train_data)
    test_rows = rd.init_test_data(test_data)
    features, features_weight = get_features(conf.feature_number, rows, hash_word, labels)
    rows = add_feature(rows, features)
    test_rows = add_feature(test_rows, features)
    return rows, test_rows, features, features_weight

# file_name, dict of word bag, file cat, features
def display_rows(rows, features):
    for row in rows:
        print row[0], row[2]
        for i in range(len(features)):
            print '\t %s:%d' %(hash_word[features[i]], row[3][i]),
    print '\n'

def normalize(vec):
    val_sum = .0
    for val in vec:
        val_sum += (val * val)
    if val_sum == 0:
        return vec
    val_sum_sqrt = math.sqrt(val_sum)
    for i in range(len(vec)):
        vec[i] /= val_sum_sqrt
    return vec
    
if __name__ == '__main__':
    train_rows, test_rows, feas, feas_weight = prepare_data(conf.data_directory)
    print 'display train_rows ...'    
    display_rows(train_rows, feas)
    print 'display test_rows ...'
    display_rows(test_rows, feas)
    
    #features = getFeatures(featureNum)
    #content = open('E:\\TextClassificationData\\content.txt', 'w')
    #temp_wordidf = features
    #for word in temp_wordidf:
    #    word, idf = word[0], word[1]
    #    content.write(word.encode('gbk')+' '+str(wordFrequency[word])+' '+str(wordDocFrequency[word])+' '+str(idf)+'\n')
    #content.close()
