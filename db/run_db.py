from weighting.doc_tfidf import DocTfidf
from pymongo import MongoClient
import datetime

class runDB():

    def __init__(self, doc_tfidf : DocTfidf):
        self.doc_tfidf = doc_tfidf

    def connect_db(self):
        # DB 연결(Docker에서 먼저 켜라)
        client = MongoClient(host='localhost', port=27017)
        # print(client.list_database_names())
        self.db = client['test'] # test db에 접근. db 이름 고민

        print("mongodb connection complete!")
        # client.admin.command('shardCollection', 'test')

        # self.db.admin.command({})
        self.today = datetime.datetime.now().date()
        # self.db.create_collection("{}".format("2023-01-20")) # 오늘 날짜 collection 생성

        self.target_collection = self.db["{}".format(self.today)] # test db 안의 오늘 날짜 collection에 접근 --> 이름이 target_collection으로 생성됨
        # if(self.db.collection.validate(db["{}".format(today)]) == False):
        #     target = db.create_collection("{}".format(today))
        # print(target)
        

    def setting(self):
        self.db["{}".format(self.today)].delete_many({}) # document 지우고 시작

        self.join_vector = self.doc_tfidf.final_word_process() # 결합 벡터 가져오기
        self.inverted_joinv = self.join_vector.T # column, index 바꾼 df

        self.hot_topic = self.doc_tfidf.hot_topic() 
        self.total_weight = 0 # hot_topic 25개의 총 빈도수 합
        self.total_weight = sum([tup[1] for tup in self.hot_topic])

        self.hot_topic_words = [tup[0] for tup in self.hot_topic] # hot_topic 25개 단어 list

        self.joinv_words = self.inverted_joinv.index.to_list() # df에 있는 단어들

        for my_word in self.joinv_words:
            if my_word in self.hot_topic_words:
                self.insert_keyword_document(my_word)

        # 가중치 순(DESC)으로 single-index 생성
        # self.db["{}".format(self.today)].create_index([('weight', -1)])
        print("hot_topic mongodb insertion complete!")

        self.joinv_doc_name = self.join_vector.index.to_list() # ['2023-01-20/0', '2023-01-20/1']

        for doc in self.joinv_doc_name:
            self.insert_each_doc_keyword(doc)

        print("each document mongodb insertion complete!")

        
    def insert_keyword_document(self, my_word):
        
        idx = [tup[0] for tup in self.hot_topic].index(my_word)
        df_idx = self.joinv_words.index(my_word)
        weight = self.hot_topic[idx][1] / self.total_weight # 나(my_word)의 가중치

        my_dict = dict() # "2022-01-20/1": 0.5 --> 이렇게 저장 할 딕셔너리

        date_idx = self.inverted_joinv.columns.to_list() # ["2023-01-20/0", "2023-01-20/1"]
        my_len = len(date_idx)

        for i in range(my_len):
            if (self.inverted_joinv.iat[df_idx, i]> 0.1):
                my_dict[date_idx[i]] = self.inverted_joinv.iat[df_idx, i]

        # sorted_my_dict = dict(sorted(my_dict.items(), key=lambda x:x[1], reverse=True)) # 각 기사 별 가중치 높은 순으로
        temp = sorted(my_dict.items(), key=lambda x:x[1], reverse=True)
        docu = {
            "_id" : my_word,
            "weight" : weight,
            "doc" : [t[0] for t in temp]
        }
        
        # collection 안에 document 넣는다.
        self.db["{}".format(self.today)].insert_one(docu)


    def insert_each_doc_keyword(self, doc):

        df_idx = self.joinv_doc_name.index(doc)

        # 핫 토픽 단어를 가진 document만 "2023-02-02/0"형태로 collection으로 저장 
        for i in range(len(self.hot_topic_words)):
            if self.join_vector.iat[df_idx, i] > 0.0:
                self.insert_values(doc)
                break


    def insert_values(self, doc):
        self.db["{}".format(doc)].drop() # collection 자체 삭제는 drop

        len_word_in_df = len(self.joinv_words) # df에 있는 단어 개수
        each_my_dict = dict()
        df_idx = self.joinv_doc_name.index(doc)
        for i in range(len_word_in_df):
            if(self.join_vector.iat[df_idx, i] > 0.0 and self.join_vector.iat[df_idx, i] < 10): # 상수 값 고민 좀
                each_my_dict[self.join_vector.columns[i]] = self.join_vector.iat[df_idx, i]

        # sorted_each_my_dict = dict(sorted(each_my_dict.items(), key=lambda x:x[1], reverse=True)) # 각 단어 별 가중치 높은 순으로
        temp = sorted(each_my_dict.items(), key=lambda x:x[1], reverse=True)
        keyword_num = len(temp)

        # 키워드를 3개 이상 가지고 있으면 top3까지 저장 / 그렇지 않으면 1개만(top1)만 저장
        if(keyword_num >= 3):
            docu = {
                "keyword": {"top1": temp[0][0], "top2": temp[1][0], "top3": temp[2][0]}
            }
        else:
            docu = {
                "keyword": {"top1": temp[0][0]}
            }
        self.db["{}".format(doc)].insert_one(docu)
        