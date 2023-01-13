from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer

class Preprocess:
    def __init__(self, s3):
        self.s3 = s3
        file = open('stopword.txt', 'r', encoding = 'utf-8')
        self.stopwords = []
        for line in file.readlines():
            self.stopwords.append(line.strip())
        self.okt = Okt()
            
    def get_s3_file(self, date, filename):
        self.s3_file = self.s3.s3_download_file(date, filename) # 작은 따옴표..
        
    def csv_to_text(self): #본문 한번에 한 줄 string으로
        self.main = self.s3_file['본문'].str.replace("[^A-Z a-z 0-9 가-힣 .]", "", regex=True)
        # arr = []
        # for line in self.main:
        #     arr.append(line)
        # self.main_text = " ".join(line for line in arr)

    def my_tokenizer(self, text):
        tokenizer = self.okt
        return [
            token for token, pos in tokenizer.pos(text)
            if pos in ['Noun', 'Alpha', 'Number'] and # 명사, 영어, 숫자
            token not in self.stopwords and len(token)>1 # 불용어 제거 이중 for문 한 문장으로 처리
        ]
        
    def give_weight(self):
        tfidf = TfidfVectorizer(tokenizer=self.my_tokenizer, decode_error = 'ignore', max_features=100, min_df=5, max_df=0.5)
        result_ft = tfidf.fit_transform(self.main)
        r = tfidf.transform(self.main)
        print(result_ft)
        print(r)
