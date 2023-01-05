import pandas
from collections import Counter
from functools import reduce
import konlpy
from konlpy.tag import *
import boto3
import io

arr = []

item_list = []
def get_headline(r):
    data_file = pandas.read_csv("s3://test-crawling-1/{}".format(r), encoding='utf-8-sig') # 상대경로
    # main = data_file[['본문']]
    main = data_file['본문'].str.replace("[^A-Za-z0-9가-힣]", "")
    i = 0
    for line in main:
        arr.append(line)
        i += 1
    
    
def preprocess():
    tokenizer = Okt()
    i = 0
    arr2 = []
    for i in arr:
        arr2.append(tokenizer.nouns(i)) # morphs로 할건지 고민
    # 2차원 배열 --> 1차원 배열로 변경
    headline_word = list(reduce(lambda x, y : x+y, arr2))
    print(headline_word)


# def get_content_from_s3(s3):
#      list = s3.list_objects(Bucket="test-crawling-1", Prefix = "data/")
#      content_list = list["Contents"]
#      bucket_name = "test-crawling-1"
#      prefix = "data/2023-01-04/2023-01-04_sbs.csv"
#      obj = s3.get_object(Bucket=bucket_name, Key=prefix)
#      df = pandas.read_csv(io.BytesIO(obj['Body'].read()))
#      get_headline(df)
#     #  item_list = []
#     #  # key값 가져오기
#     #  for content in content_list:
#     #     key = content['Key']
#     #     item_list.append(key)
#     #  return item_list[2]

def s3_connection():
        try:
            # s3 클라이언트 생성
            s3 = boto3.client(
                service_name="s3",
                region_name="ap-northeast-2",
                aws_access_key_id="AKIAQASQUQJO3YZ3GMMM",
                aws_secret_access_key="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",
            )
        except Exception as e:
            print(e)
        else:
            print("s3 bucket connected!") 
            list = s3.list_objects(Bucket="test-crawling-1", Prefix = "data/")
            content_list = list["Contents"]
            bucket_name = "test-crawling-1"
            prefix = "data/2023-01-04/2023-01-04_sbs.csv"
            obj = s3.get_object(Bucket=bucket_name, Key=prefix)
            df = pandas.read_csv(io.BytesIO(obj['Body'].read()), encoding="utf-8-sig")
            #data_file = pandas.read_csv("{}".format(df), encoding='utf-8-sig') # 상대경로
            # main = data_file[['본문']]
            main = df['본문'].str.replace("[^A-Za-z0-9가-힣]", "")
            i = 0
            for line in main:
                arr.append(line)
                i += 1

s3_connection()
# get_headline(r)
preprocess()
