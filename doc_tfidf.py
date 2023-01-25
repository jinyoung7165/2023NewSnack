from functools import reduce
import pandas as pd
class DocTfidf:
    def __init__(self, model, doc_word_dict, word_list):
        self.model = model
        self.doc_word_dict = doc_word_dict
        self.word_list = word_list

    def list_to_set(self):
        
        len_doc = len(self.doc_word_dict) # 문서 개수
        self.len_word = len(self.word_list) # 단어 개수

        self.arr = [[0]*self.len_word for _ in range(len_doc)]

        self.sorted_list = [i for i in self.word_list]
        self.sorted_list.sort()

        l = list(self.doc_word_dict) # 문서 단어들 2중 배열
        

        # result = list(dict.fromkeys(l2)) # 중복 없고 문서에 나온 단어 순인 1차원 배열 ['외교부', '일본', '정부' ...]

        for i in range(len_doc): # 문서 개수
            for j in range(self.len_word): # 단어 개수
                self.get_weight(i, j)
            print(self.arr[i])

    def get_weight(self, i, j):
        sim_sum = 0
        for word in self.word_list: # 단어 리스트
            k = 0
            for cw in self.sorted_list: # 오름차순된 단어 리스트(column 순서)
                if (word == cw): continue
                try:
                    k = self.model.wv.similarity(word, cw)
                except KeyError: k = 0
            sim_sum += k
        self.arr[i][j] = sim_sum / self.len_word