from selenium import webdriver
from tempfile import mkdtemp
import datetime
import pandas as pd
from dotenv import load_dotenv

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

#sentence = Sentence(docToText, now_date, crawl_sbs.filename)
sentence = Sentence(docToText, word2vec.model, "2023-01-20", "sbs.csv")
sentence.doc_process()
# print(sentence.docs_word_arr.keys())
# print(sentence.docs_word_arr[1])

''' . . . 3일치 언론사 뉴스로 확대 . . . '''