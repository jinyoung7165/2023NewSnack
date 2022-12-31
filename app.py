from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import os
import datetime
import boto3
from openpyxl import Workbook
import pandas as pd

DRIVER_PATH  = 'chromedriver.exe'

def crawling():
    print(os.environ)
    chrome_options = Options()
    chrome_options.add_argument( '--headless' )
    chrome_options.add_argument( '--log-level=3' )
    chrome_options.add_argument( '--disable-logging' )
    chrome_options.add_argument( '--no-sandbox' )
    chrome_options.add_argument( '--disable-gpu' )
    
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)

    item_list = []
    fields = ['url', 'author', 'date', 'headline', 'content']
    # 수집 날짜
    now_date = datetime.datetime.now().date()
    filename = '{}_{}.csv'.format(now_date,"sbs")
    
    def s3_connection():
        try:
            # s3 클라이언트 생성
            s3 = boto3.client(
                service_name="s3",
                region_name="ap-northeast-2",
                aws_access_key_id="AKIAQASQUQJO3YZ3GMMM",
                aws_secret_access_key="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",
            )
        except Exception as e:
            print(e)
        else:
            print("s3 bucket connected!") 
            return s3

    
    def current_page_items(): #전체페이지에서 각 기사의 링크, 메타데이터 저장해둠
        try:
            all_items_ul = driver.find_element(By.XPATH, "//*[@id='container']/div[2]/div[2]/ul")
            all_items = all_items_ul.find_elements(By.TAG_NAME, "li")
            for meta in all_items:
                meta_url = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'mainEntityOfPage')]")
                item_url = meta_url.get_attribute("itemid")
                
                meta_author = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'author')]")
                item_author = meta_author.get_attribute("content")
                
                meta_date = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'datePublished')]")
                item_date = meta_date.get_attribute("content")
                
                meta_headline = meta.find_element(By.XPATH, "meta[contains(@itemprop, 'headline')]")
                item_headline = meta_headline.get_attribute("content")

                item_list.append([item_url, item_author, item_date, item_headline])
        except Exception:
            return False
    
    def get_news_content(): #각 기사에서 뉴스 전문 가져옴
        text_area = driver.find_element(By.CLASS_NAME, "text_area")
        content = text_area.get_attribute("innerText")
        return content
    
    def convert_xslx():
        con = get_news_content()
        wb =  Workbook()
        ws1 = wb.active
        ws1.title = "news"
        ws1.append(["링크", "저자","날짜","제목", "본문"])
        for item in item_list:
            ws1.append(item)
        #ws1.append(con)
        wb.save(filename='{}_{}.xlsx'.format(now_date,"sbs"))
        xlsx = pd.read_excel('{}_{}.xlsx'.format(now_date,"sbs"))
        xlsx.to_csv(filename, encoding="utf-8-sig") # 한글 깨짐 해결

    # S3로 파일 업로드 함수
    def s3_upload_file():
        s3 = s3_connection()
        try:
            s3.upload_file(filename, #local 파일이름
                        "test-crawling-1", #버킷 이름
                        "data/{}/{}".format(now_date, filename)) #저장될 이름
        except Exception as e:
            print(e)        
        
    pageIdx = 1
    for _ in range(10000000):
        page_url = "https://news.sbs.co.kr/news/newsSection.do?sectionType=01&plink=SNB&cooper=SBSNEWS&pageIdx={}".format(pageIdx)
        driver.get(page_url)
        if current_page_items() == False: break
        pageIdx += 1

    for item in item_list:
        driver.get(item[0]) #각 뉴스 url
        item.append(get_news_content())
        
    s3_upload_file()
    convert_xslx()
    
crawling()
def handler(event, context):
    crawling()
    return 'Hello'