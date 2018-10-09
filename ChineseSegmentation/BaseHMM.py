#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: hiyoung 
@file: BaseHMM.py 
@time: 2018/09/22
"""

class HMM(object):

    def __init__(self):
        self.state_list = ['B','M','E','S']
        self.start_p = {}
        self.trans_p = {}
        self.emit_p = {}

        self.model_file = 'hmm_model.pkl'
        self.trained = False

    def train(self,datas,model_path=None):
        if model_path == None:
            model_path = self.model_file
        #统计状态频数
        state_dict = {}

        def init_parameters():
            for state in self.state_list:
                self.start_p[state] = 0.0
                self.trans_p[state] = {s:0.0 for s in self.state_list}
                self.emit_p[state] = {}
                state_dict[state] = 0

        def make_label(text):
            out_text = []
            if len(text) == 1:
                out_text = ['S']
            else :
                out_text += ['B']+['M']*(len(text)-2)+['E']
            return out_text

        init_parameters()
        line_nb = 0

        #监督学习方法求解参数，详情见统计学习方法10.3.1节
        for line in datas:
            line = line.strip()
            if not line:
                continue
            line_nb += 1

            word_list = [w for w in line if w != ' ']
            line_list = line.split()
            line_state = []
            for w in line_list:
                line_state.extend(make_label(w))

            assert len(line_state) == len(word_list)

            for i,v in enumerate(line_state):
                state_dict[v] += 1

                if i == 0:
                    self.start_p[v] += 1
                else :
                    self.trans_p[line_state[i-1]][v] += 1
                    self.emit_p[line_state[i]][word_list[i]] = self.emit_p[line_state[i]].get(word_list[i],0)+1.0

        self.start_p = {k: v*1.0/line_nb for k,v in self.start_p.items()}
        self.trans_p = {k:{k1: v1/state_dict[k1] for k1,v1 in v0.items()} for k,v0 in self.trans_p.items()}
        self.emit_p = {k:{k1: (v1+1)/state_dict.get(k1,1.0) for k1,v1 in v0.items()} for k,v0 in self.emit_p.items()}

        with open(model_path,'wb') as f:
            import pickle
            pickle.dump(self.start_p,f)
            pickle.dump(self.trans_p,f)
            pickle.dump(self.emit_p,f)
        self.trained = True
        print('model train done,parameters save to ',model_path)

    #读取参数模型
    def load_model(self,path):
        import pickle
        with open(path,'rb') as f:
            self.start_p = pickle.load(f)
            self.trans_p = pickle.load(f)
            self.emit_p = pickle.load(f)
        self.trained = True
        print('model parameters load done!')

    #维特比算法求解最优路径 ，详情见统计学方法10.4.2节
    def __viterbi(self,text,states,start_p,trans_p,emit_p):
        V = [{}]
        path = {}
        for y in states:
            V[0][y] = start_p[y]*emit_p[y].get(text[0],1.0)
            path[y] = [y]

        for t in range(1,len(text)):
            V.append({})
            new_path = {}

            for y in states:
                emitp = emit_p[y].get(text[t],1.0)

                (prob , state) = max([(V[t - 1][y0] * trans_p[y0].get(y, 0) * emitp, y0) \
                                      for y0 in states if V[t - 1][y0] > 0])
                V[t][y] = prob
                new_path[y] = path[state]+[y]
            path = new_path

        if emit_p['M'].get(text[-1],0) > emit_p['S'].get(text[-1],0):
            (prob,state) = max([(V[len(text)-1][y],y) for y in ('E',"M")])
        else :
            (prob,state) = max([(V[len(text)-1][y],y) for y in states])

        return (prob,path[state])

    def cut(self,text):
        if not self.trained:
            print('Error：please pre train or load model parameters')
            return

        prob,pos_list = self.__viterbi(text,self.state_list,self.start_p,self.trans_p,self.emit_p)
        begin_,next_ = 0,0

        for i, char in enumerate(text):
            pos = pos_list[i]
            if pos == 'B':
                begin_ = i
            elif pos == 'E':
                yield text[begin_:i+1]
                next_ = i+1
            elif pos == 'S':
                yield char
                next_ = i+1
        if next_ < len(text):
            yield text[next_:]


if __name__ == '__main__':
    text = '研究生命的起源'

    train_data = 'corpus/train/pku_training.utf8'
    model_file = 'hmm_model.pkl'
    hmm = HMM()
    hmm.train(open(train_data, 'r', encoding='utf-8'), model_file)
    hmm.load_model(model_file)
    print('/'.join(hmm.cut(text)))
