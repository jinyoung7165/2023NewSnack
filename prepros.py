import s3_method
from konlpy.tag import Okt

class Preprocess:
    def __init__(self, s3):
        self.s3 = s3
        file = open('stopword.txt', 'r', encoding = 'utf-8')
        self.stopwords = []
        for line in file.readlines():
            self.stopwords.append(line.strip())
            
    def get_s3_file(self, date, filename):
        self.s3_file = self.s3.s3_download_file(date, filename) # 작은 따옴표..
        
    def csv_to_text(self): #본문 한번에 한 줄 string으로
        main = self.s3_file['본문'].str.replace("[^A-Z a-z 0-9 가-힣 .]", "")
        arr = []
        for line in main:
            arr.append(line)
        self.main_text = " ".join(line for line in arr)

    def preprocess(self):
        self.token = self.my_tokenizer(self.main_text)
        # 불용어 제거 이중 for문 한 문장으로 처리
        self.result = [word for word in self.token if not word in self.stopwords]

    def my_tokenizer(self, text):
        tokenizer = Okt()
        return [
            token for token, pos in tokenizer.pos(text)
            if pos in ['Noun', 'Alpha', 'Number']
        ]
        
    # def get_word_by_freqenncy()
