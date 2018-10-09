#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: score.py 
@time: 2018/09/27
"""
def prf_score(pre_data,gold_data):
    N_count = 0   #将正类分为正或者将正类分为负
    e_count = 0   #将负类分为正
    c_count = 0   #正类分为正
    e_line_count = 0
    c_line_count = 0
    for line1,line2 in zip(gold_data,pre_data):
        list1 = line1.split(' ')
        list2 = line2.split(' ')
        count1 = len(list1)   # 标准分词数
        N_count += count1
        if line1 == line2:
            c_line_count += 1#分对的行数
            c_count += count1#分对的词数
        else:
            e_line_count += 1
            arr1 = []
            arr2 = []
            pos = 0
            for w in list1:
                arr1.append(tuple([pos, pos + len(w)]))#list1中各个单词的起始位置
                pos += len(w)
            pos = 0
            for w in list2:
                arr2.append(tuple([pos, pos + len(w)]))#list2中各个单词的起始位置
                pos += len(w)
            for tp in arr2:
                if tp in arr1:
                    c_count += 1
                else:
                    e_count += 1
    R = float(c_count) / N_count
    P = float(c_count) / (c_count + e_count)
    F = 2. * P * R / (P + R)
    ER = 1. * e_count / N_count
    print("result:")
    print('标准词数：%d个，正确词数：%d个，错误词数：%d个' %(N_count, c_count, e_count))
    print('标准行数：%d，正确行数：%d，错误行数：%d'%(c_line_count+e_line_count, c_line_count, e_line_count))
    print('Recall: %f'%(R))
    print('Precision: %f'%(P))
    print('F MEASURE: %f'%(F))
    print('ERR RATE: %f'%(ER))
    return F