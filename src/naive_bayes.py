# coding: GBK

import knn
import math

cal_precision = knn.cal_precision

train_rows = knn.train_rows
test_rows = knn.test_rows
fea_list = knn.fea_list
fea_weight = knn.fea_weight

nb_label_cnt = {}
nb_label_prob = {}

# p(y|x) = p(x|y)p(y) / p(x) = p(x1|y)p(x2|y)...p(y) / p(x)
def nb_train(train_data):
    print 'train naive bayes model ...'
    global nb_label_cnt
    global nb_label_prob
    for row in train_data:
        label = row[2]
        if label not in nb_label_cnt:
            nb_label_cnt[label] = 1
            nb_label_prob[label] = [0] * len(fea_list)
        nb_label_cnt[label] += 1
        for i in range(len(row[3])):
            if row[3][i] > 0:
                nb_label_prob[label][i] += 1
    for label in nb_label_cnt:
        label_cnt = nb_label_cnt[label]
        label_prob = nb_label_prob[label]
        for i in range(len(label_prob)):
            if label_prob[i] == 0:
                label_prob[i] = 0.01
            label_prob[i] = 1.0 * label_prob[i] / float(label_cnt)
            label_prob[i] = math.log(label_prob[i], 2.0)
    print 'finished train naive bayes model.'
    return nb_label_cnt, nb_label_prob

def cal_label_prob(vec, label):
    log_p = 0
    for i in range(len(vec)):
        if vec[i] > 0:
            log_p += nb_label_prob[label][i]
    return log_p

def nb_predict(input_data):
    global nb_label_cnt
    global nb_label_prob
    for row in input_data:
        vec = row[3]
        target = None
        target_log_p = 0
        for label in nb_label_cnt:
            log_p = cal_label_prob(vec, label)
            if target == None:
                target = label
                target_log_p = log_p
            else:
                if target_log_p < log_p:
                    target_log_p = log_p
                    target = label
        row.append(('nb_predict', target))
        print row[0], ' : ', target
    return row

def main():
    nb_train(train_rows)
    nb_predict(test_rows)
    labels = [row[2] for row in test_rows]
    labels_pred = [row[4][1] for row in test_rows]
    precision = cal_precision(labels, labels_pred)
    print 'naive bayes predication precision : %lf' %(precision)
        
if __name__ == '__main__':
    main()    