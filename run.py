import datetime
from dotenv import load_dotenv
import collections
from gensim.models import Word2Vec

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from remote.s3_method import S3
from preprocess.doc_text import DocToText
from preprocess.tokenizer import Tokenizer
from weighting.doc_tfidf import DocTfidf
from weighting.sentence import Sentence

# load .env
load_dotenv()

now_date = datetime.datetime.now().date()

''' . . . 3일치 언론사 뉴스로 확대 . . . '''
def main():
    s3 = S3() #s3 connection 1번

    docToText = DocToText(s3)
    tokenizer = Tokenizer()
    word2vec = Word2Vec.load('model')
    print(word2vec.wv.most_similar(positive=["금융"]))
    print(word2vec.wv.most_similar(positive=["테슬라"]))
    
    doc_word_dict = collections.defaultdict(list)

    delta = datetime.timedelta(days=1) # 1일 후
    end_date = datetime.datetime.now()
    today = end_date - datetime.timedelta(days=2) # 3일 전
    
    for _ in range(3):
        sentence = Sentence(docToText, tokenizer, word2vec, "{}".format(today.date()), "naver_news.csv")
        sentence.doc_process()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")
        today_name = year+"-"+month+"-"+day
        for doc_idx in sentence.docs_word_arr.keys():
            key = today_name + "/" + str(doc_idx)# "날짜/문서번호"
            doc_word_dict[key] = sentence.docs_word_arr[doc_idx]
        today += delta # 하루씩 증가
    
    doc_tfidf = DocTfidf(word2vec, doc_word_dict)
    doc_tfidf.final_word_process()
    doc_tfidf.hot_topic()

if __name__ == '__main__':
    target = main()