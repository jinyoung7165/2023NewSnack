from selenium import webdriver
from tempfile import mkdtemp
import datetime
import pandas as pd

import press_crawl

now_date = datetime.datetime.now().date()
label = ["링크", "저자","날짜","제목", "본문"]

class Crawl:
    def __init__(self, press):
        self.item_list = []
        self.press = press
        self.filename = '{}.csv'.format(press)
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = '/opt/chrome/chrome'
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
        self.driver = webdriver.Chrome("/opt/chromedriver",
                                options=self.options)
    
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
        self.convert_xslx()
        
    def convert_xslx(self):
        result = pd.DataFrame(self.item_list, columns = label)
        result.to_csv(self.filename, encoding="utf-8-sig")