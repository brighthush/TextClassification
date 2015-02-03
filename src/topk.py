# coding=GBK
"""
Created on Mon Feb 02 15:33:01 2015

@author: Bright Hush
"""

import random
#import sys

#sys.setrecursionlimit(10000)

# item is (key, value)
def kselect(items, k):
    print 'in kselect, %d %d ' %(len(items), k)    
    if k <= 0:
        return []
    #print items
    if len(items) <= k:
        return items
    index = random.randint(0, len(items) - 1)    
    pivot = items[index][1]
    right = []
    left = []
    eq = []
    for item in items:
        if item[1] > pivot:
            right.append(item)
        elif item[1] == pivot:
            eq.append(item)
        else:
            left.append(item)
    if len(right) > k:
        return kselect(right, k)
    elif len(right) == k:
        return right
    elif len(right) + len(eq) >=k:
        for i in range(k-len(right)):
            right.append(eq[i])
        return right
    else:
        right += eq
        return right + kselect(left, k - len(right))
        
def topk(items, k, ordered=False):
    topk_items = kselect(items, k)
    if not ordered:
        return topk_items
    else:
        topk_items.sort(cmp=lambda x, y: -cmp(x[1], y[1]))
        return topk_items

if __name__ == '__main__':
    a = [('a', 3.0), ('b', -9.99), ('c', 1.5), ('d', 1.7), ('e', -0.5), ('f', 10.90)]
    a_topk = topk(a, 3, True)
    print a_topk
    
