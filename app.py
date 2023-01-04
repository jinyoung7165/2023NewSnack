from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By

import datetime
import boto3
import pandas as pd
import os

def handler(event=None, context=None):
    os.chdir('/tmp')
    item_list = []
    def crawling():
        options = webdriver.ChromeOptions()
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        
        driver = webdriver.Chrome("/opt/chromedriver",
                                options=options)
  
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
        
        # S3로 파일 업로드 함수
        def s3_upload_file():
            s3 = s3_connection()
            try:
                s3.upload_file(filename, #local 파일이름
                            "test-crawling-1", #버킷 이름
                            "data/{}/{}".format(now_date, filename)) #저장될 이름
            except Exception as e:
                print(e)      
        
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
            label = ["링크", "저자","날짜","제목", "본문"]
            result = pd.DataFrame(item_list, columns = label)
            result.to_csv(filename, encoding="utf-8-sig")  
            
        pageIdx = 1
        for _ in range(10000000):
            page_url = "https://news.sbs.co.kr/news/newsSection.do?sectionType=01&plink=SNB&cooper=SBSNEWS&pageIdx={}".format(pageIdx)
            driver.get(page_url)
            if current_page_items() == False: break
            pageIdx += 1
            

        for item in item_list:
            driver.get(item[0]) #각 뉴스 url
            item.append(get_news_content())
        
        driver.quit()
        convert_xslx()
        s3_upload_file()
    
    crawling()
    return len(item_list)