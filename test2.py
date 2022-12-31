import requests
from elasticsearch import Elasticsearch
from elasticsearch import helpers


es = Elasticsearch("http://127.0.0.1:9200/")
print(es.info())

def make_idx(es, idx_name):
    if es.indices.exists(index=idx_name): # indices = index의 복수형 엘라스틱서치에서는 용어 혼란을 방지하기 위해 색인을 의미할 경우 "index", 매핑 정의공간을 의미할 경우 "indices"로 표현
        es.indices.delete(index=idx_name)
    print(es.indices.create(index=idx_name))
idx_name = 'goods'
make_idx(es, idx_name)
print(es.index)
print(es.indices)
l1 = [1,2,3,3]
print(l1.index)
print(type(es))

doc1 = {'goods_name': 'word2vec',    'price': 1000000}
doc1 = {'goods_name': 'wordvec',    'price': 1000000}
es.index(index=idx_name, doc_type='string', body=doc1, params=[])
es.indices.refresh(index=idx_name)

# 상품명에 '노트북'을 검색한다
results = es.search(index=idx_name,body={'from':0, 'size':10, 'query':{'match':{'goods_name':'hotdog'}} }, params={'allow_partial_search_results':'true'})
#result2 = es.search(index=idx_name, filter_path=['hits.hits.*'], body={'from':0, 'size':10, 'query':{'match':{'goods_name':'hot dog'}}})
for result in results['hits']['hits']:
    print('score:',result['_score'], 'source:', result['_source'])
    

words = []
for title in doc1:
    EnWords = re.sub(r"[^a-zA-Z]+", " ", str(title))
    EnWordsToken = word_tokenize(EnWords.lower())
    EnWordsTokenStop = [w for w in EnWordsToken if w not in stopWords]
    EnWordsTokenStopLemma = [lemma.lemmatize(w) for w in EnWordsTokenStop] # 표제어 추출
    words.append(EnWordsTokenStopLemma)
print(words)

requests.put("http://127.0.0.1:9200/my_index/_doc/1", doc1)
requests.put("http://127.0.0.1:9200/my_index/_doc/2", doc2)
requests.put("http://127.0.0.1:9200/my_index/_doc/3", doc3)

