from doc_text import DocToText
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas

class Sentence:
    def __init__(self, docToText: DocToText, date, filename):
        docToText.csv_to_text(date, filename)
        self.docToText = docToText
        self.docs = list(docToText.main)
        # 어제것도 갖고 와서 doc 합치는 코드 나중에 작성할 것
        # docToText 의존도 낮추기
        '''
            나중에 하기. docToText나 self.멤버 만들지 말고 함수 매개변수로 전달할지도 나중에 생각
        '''
        self.docs_df_arr = [] #전체 문서 df 저장
        
    def doc_process(self):
        # 한 문서에서 문장 리스트 뽑음
        for doc in self.docs:
            self.text = doc.split('.')
            self.preprocess(self.docToText)
            self.tfidf()
            self.get_sentence_similarity()
        print(self.docs_df_arr[3])
            
    def preprocess(self, docToText: DocToText): #각 문장에서 형태소 분석 + 불용어 제거
        tokenizer = docToText.okt
        preprocess_arr = [] #preprocess:[["앵커","어쩌고"], ]
        for line in self.text: #한 줄씩 처리 line:"앵커 어쩌고입니다"
            token = tokenizer.morphs(line) #token: 앵커, 어쩌고, 입니다
            preprocess_arr.append([word for word in token if not word in docToText.stopwords])
        
        # 각 문장당 단어 배열 -> 한 문장으로 만들기[['앵커'], ['바람']] ->['앵커 바람']
        self.word_lines = []
        for word_list in preprocess_arr:
            word_line = ' '.join(word_list)
            self.word_lines.append(word_line)

    def tfidf(self):
        tfidf = TfidfVectorizer().fit(self.word_lines)
        self.tfidf_arr = tfidf.transform(self.word_lines).toarray()

    def get_sentence_similarity(self):
        def cosine_similarity(sentence1, sentence2):
            norms = norm(sentence1) * norm(sentence2)
            if norms == 0: return 0
            return dot(sentence1, sentence2) / norms
        def nparr_to_dataframe(result_arr, line_count):
            data_frame = pandas.DataFrame(result_arr, 
                                        index=[i for i in range(line_count)], 
                                        columns = [i for i in range(line_count + 1)])
            # data_frame.sort_values(line_count, ascending=False)
            self.docs_df_arr.append(data_frame)
        arr = []
        line_count = len(self.word_lines)
        
        for i in range(line_count):
            for j in range(line_count):
                arr.append(cosine_similarity(self.tfidf_arr[i], self.tfidf_arr[j]))

        nparr = np.array(arr).reshape(line_count, line_count) # line수 * line수 배열로 만듦
        
        # 각 line별 cosine유사도 합 구해서 배열에 넣기
        total_arr = nparr.sum(axis=0)
        nparr_total = np.array(total_arr).reshape(-1,1)
        result_arr = np.hstack((nparr, nparr_total)).reshape(line_count, line_count + 1)
 
        nparr_to_dataframe(result_arr, line_count)