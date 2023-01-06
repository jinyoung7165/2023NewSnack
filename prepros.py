import pandas
from collections import Counter
from functools import reduce
from konlpy.tag import *
import boto3
import io
import s3_method


s3 = s3_method.S3()
s3_file = s3.s3_download_file("2023-01-06", 'sbs') # 작은 따옴표..
print(s3_file)