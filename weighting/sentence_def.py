from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import dot
from numpy.linalg import norm
from collections import defaultdict
from functools import lru_cache, partial
from multiprocessing import Pool, Process
import time

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from weighting.arr_util import ArrUtil
from preprocess.doc_text import DocToText
from preprocess.tokenizer import Tokenizer

@lru_cache(maxsize=3)
def sentence(docToText: DocToText, tokenizer: Tokenizer, model, date, filename):
    docToText.csv_to_text(date, filename)
    docs = list(docToText.main) # ["첫번째 문서 두번째 문장 중복 문장", "두번째 문서 두번째 문장",]
    docs_word_arr = defaultdict(list) #문서별 가진 단어 배열
    #문서별 문장 list 저장 # {0: ["첫번째", "문서", "두번째", "문장", "중복", "문장"]}
    doc_process(docs, docs_word_arr, tokenizer, model)

def doc_process(docs, docs_word_arr, tokenizer, model): # -> 모든 문서에 대해 문장유사도 df뽑을꺼 필ㅇ없는 문장 제거
    # 한 문서에서 문장 리스트 뽑음
    for idx, doc in enumerate(docs): #idx:문서 번호 - 전처리 후 문장 0개면 pass할 거라 문서번호까지 df에 나타내자
        word_lines = [] # ["첫번째 문서", "두번째 문장"]
        line_word = [] #문장별 단어 배열 #[["첫번째", "문서"], ["두번째", "문장]]
        
        row = doc.split('.')
        preprocess(row, word_lines, line_word, tokenizer)
        line_count = len(word_lines) #문장 수
        if not line_count: continue
        
        df1 = statistical_similarity(line_count, tfidf(word_lines)) #통계적 유사도
        now_t = time.time()
        df2 = semantic_similarity(line_count, line_word, model) #의미적 유사도
        print("시간", time.time() - now_t)
        sum_df = df1.add(df2) #유사도 결합
        delete_count = int(line_count*0.14) if line_count*0.14 > 1 else 1 #제거할 줄 수
        delete_idx_arr = sum_df.sort_values(by=line_count, ascending=True).head(delete_count).index #제거할 줄의 idx
        for i in range(line_count):
            if i not in delete_idx_arr:
                docs_word_arr[idx].extend(line_word[i])
                    
def preprocess(row, word_lines, line_word, tokenizer): #문서 내 각 열(row)의 문장(line) 형태소 분석 + 불용어 제거
    for line in row: #한 줄씩 처리 line:"앵커 어쩌고입니다"
        after_stopword = tokenizer.sentence_tokenizer(line)
        if after_stopword:
            line_word.append(after_stopword)
            word_lines.append(' '.join(after_stopword))

def tfidf(word_lines): #한 문서의 wordline에 대한 tfidf arr 리턴
    tfidf = TfidfVectorizer().fit(word_lines)
    return tfidf.transform(word_lines).toarray()

def statistical_similarity(line_count, tfidf_arr): #문장 수, tfidf
    def cosine_similarity(sentence1, sentence2):
        norms = norm(sentence1) * norm(sentence2)
        if norms == 0: return 0
        return dot(sentence1, sentence2) / norms

    arr = []
    for i in range(line_count):
        for j in range(line_count):
            arr.append(cosine_similarity(tfidf_arr[i], tfidf_arr[j]))

    return ArrUtil().nparr_to_dataframe(arr, line_count, line_count)

def semantic_similarity(line_count, line_word, model): #문서 내 각 행의 단어들끼리 의미적 유사도 비교
    arr = [[0]*line_count for _ in range(line_count)]
    # i행의 단어 n개* j행의 단어 m개 비교 -> ij간 단어a->단어b최대 유사도의 mean
    for i in range(line_count):
        size_a = len(line_word[i]) #A문장 단어 수
        pool = Pool(3)
        for j in range(line_count):
            if i == j: continue #같은 문장일 경우 비교x
            sum_a = 0 #i<->j행의 단어들에 대한 최대 유사도 합
            sum_a += pool.map(partial(word_comparison, line_word_j=line_word[j], model=model), line_word[i])[0]

            arr[i][j] = sum_a / size_a

    return ArrUtil().nparr_to_dataframe(arr, line_count, line_count)

def word_comparison(a, line_word_j, model): #i행의 단어 a, j행의 단어들에 대한 최대 유사도 합
    max_sim = -float('inf') #word_a와 가장 유사한 word_b와의 유사도

    for word_b in line_word_j: #j행의 단어 b
        try: 
            max_sim = max(max_sim, model.wv.similarity(a, word_b))
        except KeyError: max_sim = max(max_sim, 0)
    return max_sim