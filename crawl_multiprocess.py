from functools import partial
from selenium import webdriver
from selenium.webdriver.common.by import By
from tempfile import mkdtemp
import datetime
import pandas as pd
from dotenv import load_dotenv
import time
from multiprocessing import Manager, Pool

from s3_method import S3
# load .env
load_dotenv()

now_date = datetime.datetime.now().date()
label = ["링크", "제목", "언론사", "날짜", "기자", "본문"]
filename = 'naver_news.csv'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-tools")
options.add_argument("--no-zygote")
# self.options.add_argument(f"--user-data-dir={mkdtemp()}")
# self.options.add_argument(f"--data-path={mkdtemp()}")
# self.options.add_argument(f"--disk-cache-dir={mkdtemp()}")
# self.options.add_argument("--remote-debugging-port=9222")
driver = webdriver.Chrome(options=options)


def current_page_items(pageIdx, return_list): #전체페이지에서 각 기사의 링크, 메타데이터 저장해둠
    try:
        page_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page={}".format(pageIdx)
        driver.get(page_url)
        time.sleep(1.5)
        
        all_items_container = driver.find_element(By.XPATH, "//*[@id='section_body']")
        all_items_uls = all_items_container.find_elements(By.TAG_NAME, "ul")
        for all_items_ul in all_items_uls:
            all_items = all_items_ul.find_elements(By.XPATH, "li/dl")
            for item in all_items:
                item_meta_list = item.find_elements(By.XPATH, "dd/span")
                if item_meta_list[2].text == "1일전":
                    print("하루치 뉴스 크롤링 완료", pageIdx)
                    return False
                item_press = item_meta_list[1].text
                
                photo_or_not = item.find_elements(By.TAG_NAME, "dt")
                urls_headline = photo_or_not[1].find_element(By.TAG_NAME, "a") if len(photo_or_not) > 1 \
                    else photo_or_not[0].find_element(By.TAG_NAME, "a") #대표 사진 없는 기사

                item_url = urls_headline.get_attribute("href")
                item_headline = urls_headline.text
                
                return_list.append([item_url, item_headline, item_press]) #링크, 제목, 언론사
                        
    except Exception as e:
        print(e)
        return False

def get_news_content(idx, return_list): #각 기사에서 뉴스 전문 가져옴
    try:
        driver.get(return_list[idx][0])
        time.sleep(1.5)
        meta_area = driver.find_elements(By.XPATH, "//*[@id='ct']/div[1]/div[3]/div")
        
        item_date = meta_area[0].find_element(By.XPATH, "div/span").get_attribute("data-date-time")
        item_author = meta_area[1].text

        text_area = driver.find_element(By.XPATH, "//*[@id='dic_area']")
        content = text_area.get_attribute("innerText")
        return_list[idx] =  return_list[idx]+[item_date, item_author, content]
        
    except Exception as e:
        print(e)
        return False
        
def convert_csv(return_list):
    result = pd.DataFrame(return_list, columns = label)
    result.to_csv(filename, encoding="utf-8-sig")
    
    
def main():
    s3 = S3() #s3 connection 1번
    return_list = Manager().list()

    ''' . . . 오늘 뉴스 crawl + 파일 저장 . . . '''
    pool = Pool(3)
    pool.map(partial(current_page_items, return_list=return_list), range(1, 60)) #70p까지만 보자 -> 3시 돌려보고 false 보통 어디 페이진지 파악하기

    pool.map(partial(get_news_content, return_list=return_list), range(len(return_list)))
        
    driver.quit()
    print(len(return_list))
    convert_csv(list(return_list))
    
    s3.s3_upload_file(now_date, filename)
    # 날짜/sbs.csv
  
if __name__ == '__main__':
    target = main()
    
