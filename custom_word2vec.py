from doc_text import DocToText
from s3_method import S3
import datetime
from gensim.models import Word2Vec

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
        whole_word = []

        # 날짜들을 전역으로 하면 안되는 이유는..?
        end_date = datetime.datetime.now() # end_date는 오늘!
        now_date = end_date - datetime.timedelta(days=1) # 일단 now_date는 어제 기준..
        delta = datetime.timedelta(days=1) # 1일 후
        
        while True:
            # print(now_date.date())
            self.docToText.csv_to_text("{}".format(now_date.date()), "sbs.csv")
            self.docs = list(self.docToText.main) # ["첫번째 문서 두번째 문장", "두번째 문서 두번째 문장",]
            for doc in self.docs:
                after_stopword = self.docToText.sentence_tokenizer(doc)
                if after_stopword: whole_word.append(after_stopword)
            
            # skip-gram이 좋은 것 같다.'외교부'는 '이란'이 가장 동일하게 나옴
            self.model = Word2Vec(sentences = whole_word, min_count = 1, window = 5, workers = 4, sg = 1) 
            
            # 만약 end_date에 다다르면 while문 종료
            if(now_date.date() == end_date.date()):
                break
            now_date += delta # 1일씩 증가해주기
            

        # for train_date in (now.date(), end_date):
        #     self.docToText.csv_to_text(train_date, "sbs.csv")
        #     self.docs = list(self.docToText.main) # ["첫번째 문서 두번째 문장", "두번째 문서 두번째 문장",]
        #     whole_word = []
        #     for doc in self.docs:
        #         after_stopword = self.docToText.sentence_tokenizer(doc)
        #         if after_stopword: whole_word.append(after_stopword)
        #     self.model = Word2Vec(sentences = whole_word, min_count = 1, window = 5, workers = 4, sg = 1) # skip-gram이 좋은 것 같다.'외교부'는 '이란'이 가장 동일하게 나옴
        #     train_date = train_date + datetime.timedelta(days=1)

        print("whole_world's len : ", len(whole_word))
        # print(whole_word[0][0], self.model.wv.most_similar(whole_word[0][0]))
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