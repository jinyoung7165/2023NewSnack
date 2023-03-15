import datetime, time
from dotenv import load_dotenv
import collections
from gensim.models import Word2Vec

import sys, os, requests
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from remote.s3_method import S3
from preprocess.doc_text import DocToText
from preprocess.tokenizer import Tokenizer
from weighting.doc_tfidf import DocTfidf
from weighting.sentence import Sentence
from remote.mongo_method import RunDB
from summary.summary import Summary
# load .env
load_dotenv()

def main():
    s3 = S3() #s3 connection 1번

    docToText = DocToText(s3)
    tokenizer = Tokenizer()
    
    word2vec = Word2Vec.load('model_bulk')
    
    doc_word_dict = collections.defaultdict(list)

    delta = datetime.timedelta(days=1) # 1일 후
    end_date = datetime.datetime.now()
    today = end_date - datetime.timedelta(days=1) # 1일 전 -> 2로 바꿔야 함!!!!!!!!!!!!!!!!!!!!
    
    for _ in range(2): #3으로 바꿔야 함!!!!!!!!!!!!!!!!!!!!!!!!
        today_name = today.strftime("%Y-%m-%d")
        now_t = time.time()
        sentence = Sentence(docToText, tokenizer, word2vec, today_name, "naver_news.csv")
        sentence.doc_process()
        doc_word_dict.update(sentence.docs_word_arr)
        print(time.time()- now_t) # 하루 뉴스 490개에 210-299초
        today += delta # 하루씩 증가

    now_t = time.time()
    doc_tfidf = DocTfidf(word2vec, doc_word_dict)
    join_vector = doc_tfidf.final_word_process()
    print("joinvector", time.time()-now_t) #3일치 749초
    now_t = time.time()
    hot_topic = doc_tfidf.hot_topic()
    print("hottopic", time.time()-now_t) #4초
    # DocTfidf class 3일치 -> 18분
    now_t = time.time()
    run_db = RunDB(join_vector, hot_topic)
    run_db.setting()
    print("rundb", time.time()-now_t) #1일치 47초

    doc_main_dict = run_db.doc_dict # summary에 넘겨줄 요약 대상 {"2023-02-01/0" : "본문 내용"}
    db = run_db.db # summary에 주입할 날짜_doc collection

    now_t = time.time()
    summary = Summary(hot_topic, doc_main_dict, db)
    summary.setting()
    print("summary", time.time()-now_t) #하루치 249
    
    response = requests.get(os.environ.get('newsnack_update_uri'))
    print("today weight finished", response.text)

if __name__ == '__main__':
    target = main()