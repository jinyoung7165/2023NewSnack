import pandas
from collections import Counter
from functools import reduce
from konlpy.tag import *
import s3_method
from konlpy.tag import Okt
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

class Preprocess:
    def get_s3_file(self):
        s3 = s3_method.S3()
        self.s3_file = s3.s3_download_file("2023-01-06", 'sbs') # 작은 따옴표..
        
    def csv_to_text(self):
        main = self.s3_file['본문'].str.replace("[^A-Z a-z 0-9 가-힣]", "")
        arr = []
        i = 0;
        for line in main:
            arr.append(line)
            i = i+1
            #print(line)
        self.main_text = " ".join(line for line in arr)

    def preprocess(self):
        tokenizer = Okt()
        self.token = tokenizer.morphs(self.main_text)
        # 불용어 text(한국어는 직접 추가)
        stop_word = "의 들 와 를 으로 했습니다 이고 인 이 가 께 에 께서 에서 입니다 요".split(' ')
        # 불용어 제거 이중 for문 한 문장으로 처리
        result = [word for word in self.token if not word in stop_word]
        print(result)

    # def get_word_by_freqenncy()

preprocessed = Preprocess()
preprocessed.get_s3_file()
preprocessed.csv_to_text()
preprocessed.preprocess()