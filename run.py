import datetime
from dotenv import load_dotenv
import collections
from gensim.models import Word2Vec

import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from remote.s3_method import S3
from preprocess.doc_text import DocToText
from preprocess.tokenizer import Tokenizer
from weighting.doc_tfidf import DocTfidf
from weighting.sentence import Sentence
from db.run_db import runDB
from summary.summary import Summary
# load .env
load_dotenv()

now_date = datetime.datetime.now().date()

''' . . . 3일치 언론사 뉴스로 확대 . . . '''
def main():
    s3 = S3() #s3 connection 1번

    docToText = DocToText(s3)
    tokenizer = Tokenizer()
    
    word2vec = Word2Vec.load('model')
    # print(word2vec.wv.most_similar(positive=["금융"]))
    # print(word2vec.wv.most_similar(positive=["테슬라"]))
    
    doc_word_dict = collections.defaultdict(list)

    delta = datetime.timedelta(days=1) # 1일 후
    end_date = datetime.datetime.now()
    today = end_date - datetime.timedelta(days=1) # 1일 전.테스트용
    '''
        나중에는 today 2로 바꿔야함, naver_news_20.csv->naver_news.csv로 바꿔야함
    '''
    for _ in range(1): #3으로 바꿔야 함
        sentence = Sentence(docToText, tokenizer, word2vec, "2023-02-10", "naver_news_test.csv")
        sentence.doc_process()
        today_name = end_date.strftime("%Y-%m-%d")
        
        for doc_idx in sentence.docs_word_arr.keys():
            key = today_name + "/" + str(doc_idx)# "날짜/문서번호"
            doc_word_dict[key] = sentence.docs_word_arr[doc_idx]
        today += delta # 하루씩 증가(하루 뉴스 470개에 6-7분 소요)

    doc_tfidf = DocTfidf(word2vec, doc_word_dict)
    doc_tfidf.final_word_process()
    doc_tfidf.hot_topic()
#   DocTfidf class 이틀치(940news) ->13분

    run_db = runDB(doc_tfidf)
    run_db.connect_db()
    run_db.setting()

    # summary = Summary(docToText, doc_tfidf)
    # summary.setting()

if __name__ == '__main__':
    target = main()