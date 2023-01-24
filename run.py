from selenium import webdriver
from tempfile import mkdtemp
import datetime
import pandas as pd
from dotenv import load_dotenv
import collections
from sklearn.feature_extraction.text import TfidfVectorizer

from doc_tfidf import DocTfidf
import press_crawl
from s3_method import S3
from doc_text import DocToText
from sentence import Sentence
from custom_word2vec import customWord2Vec
# load .env
load_dotenv()

now_date = datetime.datetime.now().date()
label = ["링크", "저자","날짜","제목", "본문"]

class Crawl:
    def __init__(self, press):
        self.item_list = []
        self.press = press
        self.filename = '{}.csv'.format(press)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1280x1696")
        self.options.add_argument("--single-process")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-dev-tools")
        self.options.add_argument("--no-zygote")
        self.options.add_argument(f"--user-data-dir={mkdtemp()}")
        self.options.add_argument(f"--data-path={mkdtemp()}")
        self.options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        self.options.add_argument("--remote-debugging-port=9222")
        self.driver = webdriver.Chrome(options=self.options)
    
    def crawling(self):
        if self.press == "sbs": 
            sbs = press_crawl.Sbs()
            pageIdx = 1
            for _ in range(10000000):
                page_url = "https://news.sbs.co.kr/news/newsSection.do?sectionType=01&plink=SNB&cooper=SBSNEWS&pageIdx={}".format(pageIdx)
                self.driver.get(page_url)
                if sbs.current_page_items(self.driver, self.item_list) == False: break
                pageIdx += 1
            

            for item in self.item_list:
                self.driver.get(item[0]) #각 뉴스 url
                item.append(sbs.get_news_content(self.driver))
        
        self.driver.quit()
        self.convert_csv()
        
    def convert_csv(self):
        result = pd.DataFrame(self.item_list, columns = label)
        result.to_csv(self.filename, encoding="utf-8-sig")  

s3 = S3() #s3 connection 1번

#crawl_sbs = Crawl("sbs")
#crawl_sbs.crawling()

''' . . . 오늘 뉴스 crawl + 파일 저장 . . . '''

#s3.s3_upload_file(now_date, crawl_sbs.filename)
# 날짜/sbs.csv

docToText = DocToText(s3)

word2vec = customWord2Vec(docToText)
word2vec.custom_train()

''' . . . 1일치 언론사 뉴스 -> 전처리 . . . '''

# sentence = Sentence(docToText, now_date, crawl_sbs.filename)
# sentence = Sentence(docToText, word2vec.model, "2023-01-20", "sbs.csv")
# sentence.doc_process()
''' . . . 3일치 언론사 뉴스로 확대 . . . '''
def get_3days_word():
    doc_word_dict = collections.defaultdict(list)
    tfidf_target_word = []
    delta = datetime.timedelta(days=1) # 1일 후
    delta2 = datetime.timedelta(days=3) # 테스트를 위해 임시로 해놓은 것
    end_date = datetime.datetime.now() - delta2 # 1/21
    today = end_date - datetime.timedelta(days=1) # 1/20
    
    while True:
        sentence = Sentence(docToText, word2vec.model, "{}".format(today.date()), "sbs.csv")
        sentence.doc_process()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")
        today_name = year+"-"+month+"-"+day
        for doc_idx in sentence.docs_word_arr.keys():
            key = today_name + "/" + str(doc_idx)# "날짜/문서번호"
            doc_word_dict[key] = sentence.docs_word_arr[doc_idx]
        if (today.date() == end_date.date()):
            break
        today += delta # 하루씩 증가

    def tfidf(doc): #한 문서의 wordline에 대한 tfidf arr 리턴
        tfidf = TfidfVectorizer().fit(doc)
        return tfidf.transform(doc).toarray()
        # return tfidf.vocabulary_

    # 1차원 배열로 만들기(tf-idf를 위해서)
    for word in doc_word_dict.values():
        text = ' '.join(li for li in word)
        tfidf_target_word.append(text)

    return tfidf(tfidf_target_word)

target = get_3days_word()
# print(target)