import re
lists = """
[1단계] 다트 언어 마스터하기
02장 다트 객체지향 프로그래밍
__2.3 상속
__2.4 오버라이드
__2.5 인터페이스
__2.6 믹스인
__2.7 추상
__2.8 제네릭
__2.9 스태틱
__2.10 캐스케이드 연산자
__학습 마무리
"""
reserved = ['서론','시작하기','마무리','장','단계','부록','chapter','exercise','appendix']
graph = [word for word in re.sub('[^ A-Za-z가-힣]',' ', lists)
         .lower().split() if word not in reserved]
print(graph)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import os
import chromedriver_autoinstaller as AutoChrome

from bs4 import BeautifulSoup

DRIVER_PATH  = 'chromedriver.exe'

def crawling():

    chrome_options = Options()
    chrome_options.add_argument( '--headless' )
    chrome_options.add_argument( '--log-level=3' )
    chrome_options.add_argument( '--disable-logging' )
    chrome_options.add_argument( '--no-sandbox' )
    chrome_options.add_argument( '--disable-gpu' )
    
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)
    
    item_list = []
    
    def current_page_items():
        all_items = driver.find_elements(By.CLASS_NAME, "ss_book_box")
        for div in all_items:
            item_id = div.get_attribute("itemid")
            item_list.append(item_id)
        if len(all_items) < 50:
            return False
        return True
    
    page_num = 1
    for _ in range(10000000):
        page_url = "https://www.aladin.co.kr/shop/wbrowse.aspx?BrowseTarget=List&ViewRowsCount=50&ViewType=Detail&PublishMonth=0&SortOrder=2&page={}&Stockstatus=0&PublishDay=84&CustReviewRankStart=0&CustReviewCountStart=0&PriceFilterMax=-1&CID=351".format(page_num)
        driver.get(page_url)
        if current_page_items() == False: break
        if page_num == 1: break #test용~~~~~~~~~~~~~~~~~~~~
        page_num += 1
        print(item_list)
        
    for item in item_list:
        item_url = "https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={}".format(item)
        driver.get(item_url)
        content_all = driver.find_elements(By.CLASS_NAME, "Ere_prod_mconts_box")
        print(content_all, len(content_all))
        #contents = driver.find_element(By.XPATH, "//div[@class='Ere_prod_mconts_box'][3]//div[@id='tocTemplate']")
        #contents = contents_div.find_element(By.ID, "div_TOC_ALL")
        #contents_text = contents.get_attribute("innerText")
        #print(contents)

            
crawling() 