from doc_text import DocToText
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
        # end_date = datetime.datetime.now() # end_date는 오늘!
        # now_date = end_date - datetime.timedelta(days=1) # 일단 now_date는 어제 기준..
        # delta = datetime.timedelta(days=1) # 1일 후
        
        delta = datetime.timedelta(days=1) # 1일 후
        delta2 = datetime.timedelta(days=5)
        end_date = datetime.datetime.now() - delta2 # 1/21
        now_date = end_date - datetime.timedelta(days=1) # 1/20
        while True:
            self.docToText.csv_to_text("{}".format(now_date.date()), "sbs.csv")
            self.docs = list(self.docToText.main) # ["첫번째 문서 두번째 문장", "두번째 문서 두번째 문장",]
            for doc in self.docs:
                after_stopword = self.docToText.sentence_tokenizer(doc)
                if after_stopword: whole_word.append(after_stopword)
           
            
            # 만약 end_date에 다다르면 while문 종료
            if(now_date.date() == now_date.date()): #end_date랑 비교하는 거 하루치만 학습하려고 임시로 바꿔놨음
                break
            now_date += delta # 1일씩 증가해주기
            
         # skip-gram이 좋은 것 같다.'외교부'는 '이란'이 가장 동일하게 나옴
        self.model = Word2Vec(sentences = whole_word, vector_size=10, min_count = 1, window = 5, workers = 4, sg = 1) 