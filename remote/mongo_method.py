from pymongo import MongoClient
import datetime, os

class MongoDB:
    def __init__(self):
        client = MongoClient("mongodb+srv://{}:{}@yongyong.834oknp.mongodb.net"
                            .format(os.environ.get('mongo_username'), os.environ.get('mongo_password')))
        # print(client.list_database_names())
        self.db_doc = client['doc'] # 각 기사 키워드
        self.db_hot = client['hot'] # 핫 토픽 20개
        print("mongodb connection complete!")


class RunDB(MongoDB):
    def __init__(self, join_vector, hot_topic):
        super().__init__()
        self.join_vector = join_vector
        self.hot_topic = hot_topic
        self.today = datetime.datetime.now().date()

    def setting(self):
        self.total_weight = sum([tup[1] for tup in self.hot_topic]) # hot_topic 20개의 총 빈도수 합
        self.hot_topic_words = [tup[0] for tup in self.hot_topic] # hot_topic 20개 단어 list

        self.inverted_joinv = self.join_vector.T # column, index 바꾼 df
        self.joinv_words = self.inverted_joinv.index.to_list() # df에 있는 단어들
        self.joinv_doc_name = self.join_vector.index.to_list() # ['2023-01-20/0', '2023-01-20/1']
        self.doc_dict = dict()

        for word in self.joinv_words:
            if word in self.hot_topic_words:
                self.insert_keyword_document(word)
        print("hot topic insertion complete!") # 1초

        for doc in self.joinv_doc_name:
            self.insert_each_doc_keyword(doc)
        print("each document keyword insertion complete!") # 29초

    def insert_keyword_document(self, word): #해당 단어의 결합 벡터가 0.1이상인 문서를 db에 저장
        idx = self.hot_topic_words.index(word)
        weight = self.hot_topic[idx][1] / self.total_weight # 전체 단어 빈도 수에 비한 현재 word의 빈도 수 -> wordcloud

        doc_joinv = dict() # "2022-01-20/1": 0.5 문서명-결합벡터 저장
        doc_len = len(self.joinv_doc_name) #전체 문서 수
        df_idx = self.joinv_words.index(word) #전체 df에서 현재 단어의 위치
        for i in range(doc_len):
            if (self.inverted_joinv.iat[df_idx, i]> 0.1):
                doc_joinv[self.joinv_doc_name[i]] = self.inverted_joinv.iat[df_idx, i]

        # 해당 단어에 대한 결합벡터 높은 기사 순으로 doc 저장
        temp = sorted(doc_joinv.items(), key=lambda x:x[1], reverse=True)
        docu = {
            "_id" : word,
            "weight" : weight,
            "doc" : [t[0] for t in temp] #문서명만 저장
        }
        
        # collection 안에 document 넣는다.
        db = self.db_hot
        db[str(self.today)].insert_one(docu)

    def insert_each_doc_keyword(self, doc):
        # 핫 토픽 단어를 가진 document만 "2023-02-02/0"형태로 collection으로 저장 
        for i in range(len(self.hot_topic_words)):
            if self.join_vector.loc[doc, self.hot_topic_words[i]] > 0.0:
                self.insert_values(doc)
                break

    def insert_values(self, doc): # 해당 문서에 존재하는 단어들 중 keyword 추출
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
                "keyword": {"top1": temp[0][0], "top2": temp[1][0], "top3": temp[2][0]}
            }
        else:
            docu = {
                "keyword": {"top1": temp[0][0]}
            }
        filter = {'doc': doc} # 2023-02-10/0 == 2023-02-10/0
        db = self.db_doc
        db[doc].update_one(filter, { "$set" : docu })
        main_mongo = db[doc].find_one(filter, {'main': 1, 'doc': 1,  '_id': 0})
        main = main_mongo['main'].replace('[', '').replace(']', '') # [] 제거하고 저장
        self.doc_dict[doc] = main # {'2023-02-20' : '본문'} 형식으로 저장해서 summary에게 넘겨줌