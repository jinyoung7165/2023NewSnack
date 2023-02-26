import requests
import json
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
class Summary:
    def __init__(self, hot_topic, doc_main_arr, db_doc):
        self.hot_topic = hot_topic
        self.doc_main_arr = doc_main_arr # 요약할 기사들의 본문(사전)
        self.db_doc = db_doc

    def setting(self): 
        for key, value in self.doc_main_arr.items():
            filter = {'doc': key}
            if (self.db_doc[key].find_one({'summary': {'$exists': False}})): # summary를 하지 않은 것만 대상으로 요약
                docu = {
                    'summary': self.summarize_text(value.replace('\n', '')) # 개행 없애기(개행 너무 많으면 요약 에러 발생)
                }
                self.db_doc[key].update_one(filter, { "$set" : docu })
                print("summary")
            else:
                print("already summarized")
        print("summary update complete!")

    # 요약 함수
    def summarize_text(self, text):
        client_id = os.environ.get('summary_id')
        client_secret = os.environ.get('summary_secret')

        # 2000개 단어 기준으로 chunk 쪼개기
        text_chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]

        headers = {
            "Content-Type": "application/json; utf-8",
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
        }

        summaries = []
        
        # chunk 단위로 요약 api와 연동
        for chunk in text_chunks:

            data = {
                "document": {
                    "content": chunk,
                },
                "option": {
                    "language": "ko", # 한국어
                    "model": "news", # 뉴스 타겟
                    "summaryCount" : "3", # 3문장
                    "tone": "0" # 원문 톤
                },
            }

            res = requests.post("https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize",
                                headers=headers, data=json.dumps(data))

            rescode = res.status_code
            summary = ""
            if(rescode == 200):
                summary = json.loads(res.text)["summary"]
            else:
                print("Error : " + res.text)
            # summary = res.json()["summary"]
            summaries.append(summary)

        final_summary = "\n".join(summaries)

        return final_summary