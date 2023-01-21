from doc_text import DocToText
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas

class Sentence:
    def __init__(self, docToText: DocToText, model, date, filename):
        docToText.csv_to_text(date, filename)
        self.docToText = docToText
        self.docs = list(docToText.main) # ["첫번째 문서 두번째 문장", "두번째 문서 두번째 문장",]
        self.model = model
        
        self.doc_count = 0 #문서 수
        self.docs_df_arr = dict() #문서별 문장유사도 df 저장

    def doc_process(self):
        # 한 문서에서 문장 리스트 뽑음
        for idx, doc in enumerate(self.docs): #idx:문서 번호 - 전처리 후 문장 0개면 pass할 거라 문서번호까지 df에 나타내자
            self.word_lines = [] # ["첫번째 문서", "두번째 문장"]
            self.line_word = [] #문장별 단어 배열 #[["첫번째", "문서"], ["두번째", "문장]]
            
            row = doc.split('.')
            self.preprocess(row)
            
            self.line_count = len(self.word_lines) #문장 수
            if not self.line_count: continue
            
            df1 = self.statistical_similarity(self.tfidf()) #통계적 유사도
            df2 = self.semantic_similarity() #의미적 유사도
            if idx == 0 : print(df1, df2)
            self.docs_df_arr[idx] = pandas.merge(df1, df2)

        print(self.word_lines)
        print(self.docs_df_arr[0])
            
    def preprocess(self, row): #문서 내 각 열(row)의 문장(line) 형태소 분석 + 불용어 제거
        for line in row: #한 줄씩 처리 line:"앵커 어쩌고입니다"
            after_stopword = self.docToText.sentence_tokenizer(line)
            if after_stopword:
                self.line_word.append(after_stopword)
                self.word_lines.append(' '.join(after_stopword))

    def tfidf(self): #한 문서의 wordline에 대한 tfidf arr 리턴
        tfidf = TfidfVectorizer().fit(self.word_lines)
        return tfidf.transform(self.word_lines).toarray()

    def nparr_to_dataframe(self, arr):
        nparr = np.array(arr).reshape(self.line_count, self.line_count) # line수 * line수 배열로 만듦
        # 각 line별 유사도 합 구해서 배열에 넣기
        total_arr = nparr.sum(axis=1)
        nparr_total = np.array(total_arr).reshape(-1,1)
        result_arr = np.hstack((nparr, nparr_total)).reshape(self.line_count, self.line_count + 1)
        data_frame = pandas.DataFrame(result_arr, 
                                    index=[i for i in range(self.line_count)],
                                    columns = [i for i in range(self.line_count + 1)])
        # data_frame.sort_values(line_count, ascending=False)
        return data_frame
            
    def statistical_similarity(self, tfidf_arr): #문장 수, tfidf
        def cosine_similarity(sentence1, sentence2):
            norms = norm(sentence1) * norm(sentence2)
            if norms == 0: return 0
            return dot(sentence1, sentence2) / norms

        arr = []
        for i in range(self.line_count):
            for j in range(self.line_count):
                arr.append(cosine_similarity(tfidf_arr[i], tfidf_arr[j]))
 
        return self.nparr_to_dataframe(arr)

    def semantic_similarity(self): #문서 내 각 행의 단어들끼리 의미적 유사도 비교
        arr = [[0]*self.line_count for _ in range(self.line_count)]
        # i행의 단어 n개* j행의 단어 m개 비교 -> ij간 단어a->단어b최대 유사도의 mean
        for i in range(self.line_count):
            size_a = len(self.line_word[i]) #A문장 단어 수
            for j in range(self.line_count):
                if i == j: continue #같은 문장일 경우 비교x
                sum_a = 0 #i<->j행의 단어들에 대한 최대 유사도 합
                for word_a in self.line_word[i]: #i행의 단어 a
                    max_sim = -float('inf') #word_a와 가장 유사한 word_b와의 유사도
                    
                    for word_b in self.line_word[j]: #j행의 단어 b
                        try: 
                            max_sim = max(max_sim, self.model.wv.similarity(word_a, word_b))
                        except KeyError: max_sim = max(max_sim, 0)
                    sum_a += max_sim
                    
                arr[i][j] = sum_a / size_a
        
        return self.nparr_to_dataframe(arr)