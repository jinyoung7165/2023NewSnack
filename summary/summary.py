import requests
import json
import os
from dotenv import load_dotenv
from preprocess.doc_text import DocToText
from weighting.doc_tfidf import DocTfidf

load_dotenv()
class Summary:
    def __init__(self, docToText : DocToText, docTfidf : DocTfidf):
        self.docToText = docToText
        self.docTfidf = docTfidf

    def setting(self):
        self.document = list(self.docToText.main)
        hot_topic_words = [tup[0] for tup in self.docTfidf.hot_topic()] # hot_topic 25개 단어 list
        
        doc_len = len(self.document) # 기사 개수

        dup_arr = [] # 핫토픽이 중복되는 문서는 요약 한 번만 하면 되므로 중복 방지
        for i in range(len(hot_topic_words)): 
            for j in range(doc_len):
                if hot_topic_words[i] in self.document[j]:
                    if (j in dup_arr): continue
                    # if (j != 26): continue
                    dup_arr.append(j)
                    my_summary = ""
                    my_doc_len = len(self.document[j])
                    # 4000자 까지는 가능
                    if (my_doc_len > 2000):
                        my_summary += self.over_2000words(self.document[j], my_doc_len)
                    else:
                        my_summary += self.execute_summary(self.document[j])
                    print(my_summary, j)
                    print()

    def over_2000words(self, content, doc_len):
        text = content.split('.') 
        half_len = doc_len / 2
        idx = 0
        first = ""
        remainder = ""
        temp = ""
        for p in range(doc_len):
            temp += text[p]
            if(len(temp) >= half_len):
                idx = p
                break
        first += '.'.join(li for li in text[0:idx])
        remainder += '.'.join(li for li in text[idx:])
        temp = ""
        if(len(remainder) > 2000):
            temp += self.over_2000words(remainder, len(remainder))
            print("22")
            return temp
        print("2")
        return (self.execute_summary(first) + self.execute_summary(remainder))

    def execute_summary(self, target_content):
        client_id = os.environ.get('summary_id')
        client_secret = os.environ.get('summary_secret')
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/json"
        }

        language = "ko"
        url = 'https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize'
        model = "news" # Model used for summaries (general, news)
        tone = "0" # Converts the tone of the summarized result. (0, 1, 2, 3) 원문 어투 유지.
        summaryCount = "3" # 3줄 요약

        content = target_content
        data = {
            "document": {
            "content" : content
            },
            "option": {
            "language": language,
            "model": model,
            "tone": tone,
            "summaryCount" : summaryCount
            }
        }
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        rescode = response.status_code
        my_summary = ""
        if(rescode == 200):
            my_summary += json.loads(response.text)["summary"]
        else:
            print("Error : " + response.text)
        
        return my_summary
            
# summary = Summary()
# summary.test_get_document()