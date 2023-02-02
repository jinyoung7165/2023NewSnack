import datetime
import os
from dotenv import load_dotenv

from training.s3_method import S3
from crawl import Crawl
# load .env
load_dotenv()


now_date = datetime.datetime.now().date()
label = ["링크", "저자","날짜","제목", "본문"]

def handler(event=None, context=None):
    os.chdir('/tmp')
    s3 = S3() #s3 connection 1번

    crawl_sbs = Crawl("sbs")
    crawl_sbs.crawling()
    ''' . . . 다른 언론사 crawl . . . '''

    s3.s3_upload_file(now_date, crawl_sbs.filename)
    ''' . . . 다른 언론사 파일 저장 . . . '''
    
    ''' 전처리 '''
    return now_date