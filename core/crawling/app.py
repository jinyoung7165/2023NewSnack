import os
from dotenv import load_dotenv
from crawl import crawl
# load .env
load_dotenv()

def handler(event=None, context=None):
    os.chdir('/tmp')
    today = crawl()
    return {
        "date": today
    }