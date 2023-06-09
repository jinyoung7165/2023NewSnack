from bson import ObjectId
from pymongo import MongoClient
import datetime, os, re

class MongoDB:
    def __init__(self, db=None):
        today = str(datetime.datetime.now().date())
        if db is None: #crawler에서 호출
            client = MongoClient("mongodb+srv://{}:{}@yongyong.834oknp.mongodb.net"
                                .format(os.environ.get('mongo_username'), os.environ.get('mongo_password')))
            self.db = client['newsnack'] #db 접근
            self.doc_c = self.db['{}_doc'.format(today)] # 오늘 문서 저장하는 doc collection
        else: #run.py에서 주입
            self.db = db
            self.hot_c = db['{}_hot'.format(today)] # 오늘 핫 토픽 저장하는 hot collection
        print("mongodb connection complete!")

    def get_all_docs(self, date): # 날짜_doc의 모든 문서 [[id, main], [id, main]]
        doc_c = self.db['{}_doc'.format(date)]
        date_docs = doc_c.find(None, {'_id': 1, 'main': 1, 'title': 1})
        date_docs_list = []
        for doc in date_docs:
            id = str(doc['_id']) #{"_id": ObjectId(id)}
            main = re.sub('[^A-Z a-z 0-9 가-힣 .]', '', doc['main'])
            title = re.sub('[^A-Z a-z 0-9 가-힣 .]', '', doc['title'])
            main += "." + title + "." + title + "." + title #제목 가중치 3배
            date_docs_list.append([id, main])
            
        return date_docs_list

class RunDB:
    def __init__(self, db: MongoDB, join_vector, hot_topic):
        self.db = db
        self.hot_c = db.hot_c
        self.join_vector = join_vector
        self.hot_topic = hot_topic

    def setting(self):
        self.total_weight = sum([tup[1] for tup in self.hot_topic]) # hot_topic 20개의 총 빈도수 합
        self.hot_topic_words = [tup[0] for tup in self.hot_topic] # hot_topic 20개 단어 list

        self.inverted_joinv = self.join_vector.T # column, index 바꾼 df
        self.joinv_words = self.inverted_joinv.index.to_list() # df에 있는 단어들
        self.joinv_doc_name = self.join_vector.index.to_list() # ['2023-01-20_doc/0', '2023-01-20_doc/1']
        self.doc_dict = dict()

        hots = []
        for word in self.joinv_words:
            if word in self.hot_topic_words:
                hots.append(self.hottopic_document(word))
        # 날짜_hot collection 안에 document 넣는다.
        self.hot_c.insert_many(hots)
        print("hot topic insertion complete!") # 1초

        for doc in self.joinv_doc_name:
            self.insert_each_doc_keyword(doc)
        print("each document keyword insertion complete!") # 29초

    def hottopic_document(self, word): #해당 단어의 결합 벡터가 0.1이상인 문서를 db에 저장
        idx = self.hot_topic_words.index(word)
        weight = self.hot_topic[idx][1] / self.total_weight # 전체 단어 빈도 수에 비한 현재 word의 빈도 수 -> wordcloud

        doc_joinv = dict() # "2022-01-20_doc/1": 0.5 문서명-결합벡터 저장
        doc_len = len(self.joinv_doc_name) #전체 문서 수
        df_idx = self.joinv_words.index(word) #전체 df에서 현재 단어의 위치
        for i in range(doc_len):
            if (self.inverted_joinv.iat[df_idx, i]> 0.1):
                doc_joinv[self.joinv_doc_name[i]] = self.inverted_joinv.iat[df_idx, i]

        # 해당 단어에 대한 결합벡터 높은 기사 순으로 doc 저장
        temp = sorted(doc_joinv.items(), key=lambda x:x[1], reverse=True)
        hot = {
            "word" : word,
            "weight" : weight,
            "doc" : [{"ref": t[0].split("/")[0], "_id": t[0].split("/")[1]} for t in temp] # 날짜_doc, _id
        }
        
        return hot

    def insert_each_doc_keyword(self, doc):
        # 핫 토픽 단어를 가진 document만 "2023-02-02_doc/0"형태로 collection으로 저장 
        for i in range(len(self.hot_topic_words)):
            if self.join_vector.loc[doc, self.hot_topic_words[i]] > 0.0:
                self.insert_keyword(doc)
                break

    def insert_keyword(self, doc): # 해당 문서에 존재하는 단어들 중 keyword 추출        
        date, id = doc.split('/') #collection, _id
        doc_c = self.db.db[date] # 해당 hot topic 문서를 가진 doc collection
        if (doc_c.find_one({'_id': ObjectId(id), 'keyword': {'$exists': True }})): return #이미 keyword가 존재하는 doc이면 return
        
        word_joinv = dict() # 해당 문서에 존재하는 단어-결합벡터 저장
        len_word_in_df = len(self.joinv_words) # df에 있는 전체 단어 수
        df_idx = self.joinv_doc_name.index(doc)
        for i in range(len_word_in_df):
            if(self.join_vector.iat[df_idx, i] > 0.0): #결합벡터가 0보다 크면 keyword 후보로 등록
                word_joinv[self.join_vector.columns[i]] = self.join_vector.iat[df_idx, i]

        del word_joinv['total'] # total은 지우기
        temp = sorted(word_joinv.items(), key=lambda x:x[1], reverse=True)
        keyword_num = len(temp)

        # 키워드를 3개 이상 가지고 있으면 top3까지 저장 / 그렇지 않으면 1개만(top1)만 저장
        if(keyword_num >= 3):
            docu = {
                "keyword": [temp[0][0], temp[1][0], temp[2][0]]
            }
        else:
            docu = {
                "keyword": [temp[0][0]]
            }
        filter = {'_id': ObjectId(id)}
        doc_c.update_one(filter, { "$set" : docu })
        
        main_mongo = doc_c.find_one(filter, {'main': 1, 'doc': 1,  '_id': 1})
        main = re.sub('[^A-Z a-z 0-9 가-힣 · % .]', '', main_mongo['main'])
        self.doc_dict[doc] = main # {'2023-02-20/_id' : '본문'} 형식으로 저장해서 summary에게 넘겨줌