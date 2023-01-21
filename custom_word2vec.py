from doc_text import DocToText
from s3_method import S3
import datetime
from gensim.models import Word2Vec

now_date = datetime.datetime.now().date()
class customWord2Vec:
    def __init__(self, docToText: DocToText):
        self.docToText = docToText
        
    def custom_train(self):
        #while True:
        date = "2023-01-20" 
        '''
        date 특정 날짜까지 계속 증가하게 하는 코드 만들기(start, end 날짜 알 때)
        병렬 처리
        '''
        self.docToText.csv_to_text(date, "sbs.csv")
        self.docs = list(self.docToText.main) # ["첫번째 문서 두번째 문장", "두번째 문서 두번째 문장",]
        whole_word = []
        for doc in self.docs:
            after_stopword = self.docToText.sentence_tokenizer(doc)
            if after_stopword: whole_word.append(after_stopword)
        self.model = Word2Vec(sentences = whole_word, min_count = 1, window = 5, workers = 4, sg = 0)
        
    # def word2vec(self): 
    #     # size = 워드 벡터의 특징 값. 즉, 임베딩 된 벡터의 차원.
    #     # window = 컨텍스트 윈도우 크기
    #     # min_count = 단어 최소 빈도 수 제한 (빈도가 적은 단어들은 학습하지 않는다.)
    #     # workers = 학습을 위한 프로세스 수
    #     # sg = 0은 CBOW, 1은 Skip-gram.

    #     # 전처리한 단어를 포함한 2차원 배열 array 학습 시키기
    #     self.model = Word2Vec(sentences = self.line_word, min_count = 1, window = 5, workers = 4, sg = 0)
# s = S3()
# d = DocToText(s)
# w = customWord2Vec(d)
# w.custom_train()