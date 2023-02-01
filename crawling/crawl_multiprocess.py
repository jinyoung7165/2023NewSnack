from functools import partial
import datetime
import pandas as pd
from dotenv import load_dotenv
import time
from multiprocessing import Manager, Pool
from bs4 import BeautifulSoup
import requests
import re
from s3_method import S3
# load .env
load_dotenv()

date = datetime.datetime.now()

label = ["링크", "언론사", "제목", "날짜", "본문"]
filename = 'naver_news.csv'
year = date.strftime("%Y")
month = date.strftime("%m")
day = date.strftime("%d")
today = year+month+day

now_date = date.date()
def current_page_items(pageIdx, return_list): #전체페이지에서 각 기사의 링크, 메타데이터 저장해둠
    try:
        page_url = "https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=101&date={}&page={}".format(today, pageIdx)
        all_list = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
        all_html = BeautifulSoup(all_list.text, 'html.parser')
        time.sleep(1.5)
        
        all_items = all_html.select("div.list_body.newsflash_body > ul.type06_headline > li > dl")
        
        for item in all_items:
            item_press = item.select("dd > span.writing")[0].text
            photo_or_not = item.select("dt")
            url_headline = photo_or_not[1].find("a") if len(photo_or_not) > 1 \
                else photo_or_not[0].find("a") #대표 사진 없는 기사
            item_url = url_headline.get("href")
            return_list.append([item_url, item_press]) #링크, 언론사
                        
    except Exception as e:
        print(e)
        return False

def get_news_content(idx, return_list): #각 기사에서 뉴스 전문 가져옴
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
    
    
def crawl():
    print(today, "오늘의 crawl 시작")
    return_list = Manager().list()

    ''' . . . 오늘 뉴스 crawl + 파일 저장 . . . '''
    pool = Pool(3)
    pool.map(partial(current_page_items, return_list=return_list), range(1, 50)) #70p까지만 보자 -> 3시 돌려보고 false 보통 어디 페이진지 파악하기

    pool.map(partial(get_news_content, return_list=return_list), range(len(return_list)))

    convert_csv(list(return_list))
  
if __name__ == '__main__':
    s3 = S3() #s3 connection 1번
    target = crawl()
    s3.s3_upload_file(now_date, "naver_news.csv")