#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: BaseDict.py
@time: 2018/09/20
"""

class FMM(object):
    def __init__(self,word_dict):
        self.word_dict = word_dict
        self.window_size = self.__getMaxLen()

    def __getMaxLen(self):
        return max(map(len,[w for w in self.word_dict]))

    def cut(self,text):
        result = []
        index = 0
        text_size = len(text)
        while text_size > index:
            for size in range(self.window_size+index,index,-1):
                piece = text[index:size]
                if piece in self.word_dict:
                    index = size - 1
                    break
            index = index + 1
            result.append(piece)
        return result

class RMM(object):
    def __init__(self,word_dict):
        self.word_dict = word_dict
        self.window_size = self.__getMaxLen()

    def __getMaxLen(self):
        return max(map(len,[w for w in self.word_dict]))

    def cut(self,text):
        result = []
        index = len(text)
        window_size = min(index,self.window_size)
        while index > 0:
            for size in range(index-window_size,index):
                piece = text[size:index]
                if piece in self.word_dict:
                    index = size + 1
                    break
            index = index - 1
            result.append(piece)
        result.reverse()
        return result

class BIMM(object):
    def __init__(self,word_dict):
        self.word_dict = word_dict
        self.FMM = FMM(self.word_dict)
        self.RMM = RMM(self.word_dict)

    def cut(self,text):
        res_fmm = self.FMM.cut(text)
        res_rmm = self.RMM.cut(text)
        if len(res_fmm) == len(res_rmm):
            if res_fmm == res_rmm :
                return res_fmm
            else:
                f_word_count = len([w for w in res_fmm if len(w)==1])
                r_word_count = len([w for w in res_rmm if len(w)==1])
                return res_fmm if f_word_count < r_word_count else res_rmm
        else:
            return res_fmm if len(res_fmm) < len(res_rmm) else res_rmm


if __name__ == '__main__':
    # Get word dict to list(),this is jieba dict.txt
    dic_path = 'D:\ProgramData\Anaconda3\Lib\site-packages\jieba\dict.txt'
    dic = []
    with open(dic_path, 'r',encoding='utf-8') as f:
        for line in f:
            word = line.strip().split()
            dic.append(word[0])

    text = '研究生命的起源'
    #     tokenizer = FMM(dic)
    #     tokenizer = RMM(dic)
    tokenizer = BIMM(dic)
    print('/'.join(tokenizer.cut(text)))
