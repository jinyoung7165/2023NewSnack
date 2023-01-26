from konlpy.tag import Okt

class DocToText:
    def __init__(self, s3):
        self.s3 = s3
        file = open('stopword.txt', 'r', encoding = 'utf-8')
        self.stopwords = []
        for line in file.readlines():
            self.stopwords.append(line.strip())
        self.okt = Okt()

    def csv_to_text(self, date, filename): #본문 한번에 한 줄 string으로
        self.s3_file = self.s3.s3_download_file(date, filename) # 작은 따옴표..
        self.main = self.s3_file['본문'].str.replace("[^A-Z a-z 0-9 가-힣 .]", "", regex=True)
        self.title = self.s3_file['제목'].str.replace("[^A-Z a-z 0-9 가-힣 .]", "", regex=True)

    def sentence_tokenizer(self, text):
        tokenizer = self.okt
        return [
            token for token, pos in tokenizer.pos(text, norm=True, stem=True)
            if pos in ['Noun', 'Alpha', 'Number', 'Verb'] and # 명사, 영어, 숫자, 동사
            token not in self.stopwords # 불용어 제거 이중 for문 한 문장으로 처리
        ]
        
    def keyword_tokenizer(self, text):
        tokenizer = self.okt
        return [
            token for token, pos in tokenizer.pos(text)
            if pos in ['Noun', 'Alpha', 'Number'] and # 명사, 영어, 숫자
            token not in self.stopwords and len(token)>1 # 불용어 제거 이중 for문 한 문장으로 처리
        ]