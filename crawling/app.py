import datetime
import os
from dotenv import load_dotenv
from crawl import crawl
# load .env
load_dotenv()


now_date = datetime.datetime.now().date()

def handler(event=None, context=None):
    os.chdir('/tmp')
    crawl()
    return now_date