#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: Test.py 
@time: 2018/09/26
"""

import os
from BaseHMM import HMM
from BaseDict import BIMM
from score import prf_score
import jieba

#for BaseHMM
def load_trian(root_path,file_list):
    train_data = []
    # train_path = 'corpus/train/'
    for file in file_list:
        with open(root_path+file,'r',encoding='utf-8') as f:
            for line in f:
                train_data.append(line.strip().replace('\u3000',' '))
    return train_data

def load_test(gold_path,test_path,gold_list,test_list):
    # gold_path = "corpus/val/gold/"
    # test_path = "corpus/val/test/"

    gold_data = []
    test_data = []

    for file in test_list:
        with open(test_path+file,'r',encoding='utf-8') as f:
            for line in f:
                test_data.append(line.strip().replace('\u3000',' '))

    for file in gold_list:
        with open(gold_path+file,'r',encoding='utf-8') as f:
            for line in f:
                gold_data.append(line.strip().replace('\u3000',' '))

    return test_data,gold_data

if __name__ == '__main__':
    model_file = 'hmm_model.pkl'
    train_path = 'corpus/train/'
    gold_path = 'corpus/val/gold/'
    test_path = 'corpus/val/test/'

    train = load_trian(train_path,['pku_training.utf8'])
    test , gold = load_test(gold_path,test_path,['pku_test_gold.utf8'],['pku_test.utf8'])
    hmm = HMM()
    hmm.train(train,model_file)
    hmm.load_model(model_file)

    pre_hmm_data = []
    pre_jieba_data = []
    for t in test:
        if len(t) == 0:
            continue
        pre_hmm_data.append(' '.join(hmm.cut(t)))
        pre_jieba_data.append(' '.join(jieba.cut(t)))

    prf_score(pre_hmm_data,gold)
    print('-----------------------')
    prf_score(pre_jieba_data,gold)

