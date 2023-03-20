import datetime, time, collections, sys, os, requests
from dotenv import load_dotenv
from gensim.models import Word2Vec
from pymongo import MongoClient

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocess.tokenizer import Tokenizer
from weighting.doc_tfidf import DocTfidf
from weighting.sentence import Sentence
from remote.mongo_method import MongoDB, RunDB
from summary.summary import Summary
# load .env
load_dotenv()

def main():
    client = MongoClient("mongodb+srv://{}:{}@yongyong.834oknp.mongodb.net"
                .format(os.environ.get('mongo_username'), os.environ.get('mongo_password')))
    db = client['newsnack'] #db 접근
    mongodb = MongoDB(db)
    
    tokenizer = Tokenizer()
    word2vec = Word2Vec.load('model_bulk')
    
    doc_word_dict = collections.defaultdict(list)

    delta = datetime.timedelta(days=1) # 1일 후
    end_date = datetime.datetime.now()
    today = end_date - datetime.timedelta(days=2) #이틀 전부터 실행
    today = end_date
    
    for _ in range(1):
        today_name = today.strftime("%Y-%m-%d")
        now_t = time.time()
        sentence = Sentence(mongodb, tokenizer, word2vec, today_name)
        sentence.doc_process()
        doc_word_dict.update(sentence.docs_word_arr) #date/_idx : ['단어1','단어2']
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
    run_db = RunDB(mongodb, join_vector, hot_topic)
    run_db.setting()
    print("rundb", time.time()-now_t) #1일치 47초

    doc_main_dict = run_db.doc_dict # summary에 넘겨줄 요약 대상 {"2023-02-01/_id" : "본문 내용"}

    now_t = time.time()
    summary = Summary(db, hot_topic, doc_main_dict)
    summary.setting()
    print("summary", time.time()-now_t) #하루치 249
    
    response = requests.get(os.environ.get('newsnack_update_uri'))
    print("today weight finished", response.text)

if __name__ == '__main__':
    target = main()