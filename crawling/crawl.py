import datetime
import pandas as pd
import time
from threading import Thread
from multiprocessing import Manager, Process
from bs4 import BeautifulSoup
import requests
import re

from dotenv import load_dotenv
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from remote.s3_method import S3
from remote.mongo_method import MongoDB

# load .env
load_dotenv()

date = datetime.datetime.now()

label = ["링크", "언론사", "이미지", "제목", "날짜", "본문"]
filename = 'naver_news.csv'
today = date.strftime("%Y%m%d")

now_date = str(date.date())
def current_page_items(pageIdx, return_list): #전체페이지에서 각 기사의 링크, 메타데이터 저장해둠
    try:
        page_url = "https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=101&date={}&page={}".format(today, pageIdx)
        all_list = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        all_html = BeautifulSoup(all_list.text, 'html.parser')
        time.sleep(1.5)
        
        all_items = all_html.select("div.list_body.newsflash_body > ul.type06_headline > li > dl")
                
        def get_press_url_thread(item, return_list):
            item_press = item.select("dd > span.writing")[0].text
            photo_or_not = item.select("dt")
            url_headline = photo_or_not[1].find("a") if len(photo_or_not) > 1 \
                else photo_or_not[0].find("a") #대표 사진 없는 기사
            item_url = url_headline.get("href")
            item_image = photo_or_not[0].select_one("a > img").attrs["src"] if len(photo_or_not) > 1 \
                else None #대표 사진 없는 기사
            if item_image: item_image = item_image[:item_image.find('?type=')]
            return_list.append([item_url, item_press, item_image]) #링크, 언론사, 사진

        ths = []
        for item in all_items:
            th = Thread(target=get_press_url_thread, args=(item, return_list))
            th.start()
            ths.append(th)
        for th in ths:
            th.join()

    except Exception as e:
        print(e)
        return False

def get_news_content_thread(idx, return_list, return_len): #각 기사에서 뉴스 전문 가져옴(idx 3개씩 건너뛰면서 순회)
    ths = []
    for idx_thread in range(idx, return_len, return_len//2 - 1):
        th = Thread(target=get_news_content, args=(idx_thread, return_list))
        th.start()
        ths.append(th)
    for th in ths:
        th.join()
                    
            
def get_news_content(idx, return_list):
    try:
        news = requests.get(return_list[idx][0], headers={'User-Agent': 'Mozilla/5.0'})
        news_html = BeautifulSoup(news.text, "html.parser")
        time.sleep(1.5)
       
        # html태그제거 및 텍스트 다듬기
        pattern1 = '<[^>]*>'
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        
        # 뉴스 제목 가져오기
        item_title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if item_title == None:
            item_title = news_html.select_one("#content > div.end_ct > div > h2")

        # 날짜 가져오기
        try:
            html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            item_date = html_date.attrs['data-date-time']
        except AttributeError:
            item_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            item_date = re.sub(pattern=pattern1,repl='',string=str(item_date))

        # 본문 가져오기
        text_area = news_html.select("div#dic_area")
        if len(text_area) == 0: text_area = news_html.select("#articeBody")
        content = ''.join(str(text_area))

        item_title = re.sub(pattern=pattern1, repl='', string=str(item_title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        content = content.replace(pattern2, '')

        return_list[idx] =  return_list[idx]+[item_title, item_date, content]
        
    except Exception as e:
        print(e)
        return False
        
def convert_csv(return_list):
    result = pd.DataFrame(return_list, columns = label)
    result.to_csv(filename, encoding="utf-8-sig")
    

def save_in_mongo(mongodb, return_list):
    for i in range(len(return_list)):
        doc_name = now_date + "/" + str(i)
        docu = {
            'doc': doc_name, # 2023-02-10/0
            'link': return_list[i][0], # 링크
            'press': return_list[i][1], # 언론사
            'image': return_list[i][2], # 이미지
            'title': return_list[i][3], # 제목
            'date': return_list[i][4], # 날짜 ('2023-02-21 12:53:01' 형식)
            'main': return_list[i][5], # 본문
        }
        mongodb.insert_one(docu) #날짜_doc collection에 삽입

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
            
def crawl():
    s3 = S3() #s3 connection 1번
    mongodb = MongoDB().doc_c #mongo doc collection
    
    print(today, "오늘의 crawl 시작")
    return_list = Manager().list()

    ''' . . . 오늘 뉴스 crawl + 파일 저장 . . . '''
    plimit = 20
    print("process limit: ", plimit)
    # 멀티프로세싱 
    processes = []
 
    for i in range(1, 50):
        current_page_items(i, return_list)
    
    for i in range(len(return_list)//2 - 1):
        process = Process(target=get_news_content_thread, args=(i, return_list, len(return_list)))
        processes.append(process)
      
    for process_chuck in chunks(processes, plimit):
        # 멀티프로세스 시작
        for process in process_chuck:
            process.start()
        # 멀티프로세스 종료
        for process in process_chuck:
            process.join()
    
        
    convert_csv(list(return_list))
    save_in_mongo(mongodb, list(return_list))
    mongodb.create_index('keyword')
    
    s3.s3_upload_file(now_date, "naver_news.csv")
    
    return today
    
if __name__ == '__main__':
    target = crawl()