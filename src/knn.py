# coding=GBK
import configuration as conf
import features as feas
from topk import topk

train_rows, test_rows, fea_list, fea_weight = feas.prepare_data(conf.data_directory)

def data_normalize():
    for row in train_rows:
        row[3] = feas.normalize(row[3])
        #for i in range(len(row[3])):
        #    row[3][i] *= fea_weight[i]
    for row in test_rows:
        row[3] = feas.normalize(row[3])
        #for i in range(len(row[3])):
        #    row[3][i] *= fea_weight[i]

def similarity(vectora, vectorb):
    sim = 0
    for i in xrange(len(vectora)):
        sim += vectora[i]*vectorb[i]
    return sim

def topk_sim(input_vec, k_value):
    neighbours = []
    for row in train_rows:
        sim = similarity(input_vec, row[3])
        neighbours.append((row, sim))
        #neighbours.append((row[2], sim))
    neigh_topk = topk(neighbours, k_value, True)
    #neigh_topk = neighbours
    for neigh in neigh_topk:
        row = neigh[0]
        sim = neigh[1]
        #print row[2], sim
    return neigh_topk

def choose_label(neigh_topk):
    labels_cnt = {}
    labels_sim = {}
    for neigh in neigh_topk:
        row = neigh[0]
        sim = neigh[1]
        label = row[2]
        if label not in labels_cnt:
            labels_cnt[label] = 0
            labels_sim[label] = 0
        labels_cnt[label] += 1
        labels_sim[label] += sim
    target_cnt = 0
    target_sim = 0
    target = -1
    for label in labels_cnt:
        if labels_cnt[label] > target_cnt:
            target = label
            target_cnt = labels_cnt[label]
            target_sim = labels_sim[label]
        elif labels_cnt[label] == target_cnt:
            if labels_sim[label] > target_sim:
                target = label
                target_sim = labels_sim[label]
    return target, target_cnt, target_sim

def knn_predict(input_data, k_value):
    for row in input_data:
        input_vec = row[3]
        neigh_topk = topk_sim(input_vec, k_value)
        target, target_cnt, target_sim = choose_label(neigh_topk)
        row.append(('knn_predict', target))
        print row[0], row[2], 'knn_predict :', target
    return input_data

def cal_precision(label, label_pred):
    if len(label) != len(label_pred):
        print 'label and label_pred with different length.'
        exit()
    right = 0
    for i in range(len(label)):
        if label[i] == label_pred[i]:
            right += 1
    right = 1.0 * right / float(len(label))
    return right

if __name__ == '__main__':
    data_normalize()
    knn_out = knn_predict(test_rows, conf.knn_k)
    labels = [ row[2] for row in knn_out ]
    labels_pred = [ row[-1][1] for row in knn_out ]
    precision = cal_precision(labels, labels_pred)
    print 'knn predication precision : %lf' %(precision)
    