# 경량 ubuntu
# FROM alpine:3.14 

FROM python:3

# apt init
ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl

# install java
ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk/jre"
# RUN apt-get install -y openjdk-8-jdk
RUN apt-get install -y g++ default-jdk
# installing python3 and pip3
# RUN apt-get install -y python3-pip python3-dev

# apt cleanse
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# timezone
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# make workspace for konlpy
RUN mkdir -p /workspace
WORKDIR /workspace

# install konlpy dependencies: jpype, konlpy, with mecab module
RUN pip install jpype1-py3 konlpy
RUN cd /workspace && \
    curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash -s

# app 디렉토리 생성
RUN mkdir -p /app

#RUN, CMD, ENTRYPOINT의 명령이 실행될 디렉터리
WORKDIR /app

COPY .env ./
COPY remote ./remote
COPY preprocess ./preprocess
COPY summary ./summary

COPY requirements.txt  ./
RUN pip install -r requirements.txt

COPY weighting/sentence.py ./weighting/
COPY weighting/arr_util.py ./weighting/
COPY weighting/doc_tfidf.py ./weighting/

COPY model_bulk ./
COPY stopword.txt ./
COPY run.py ./

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "python3", "run.py" ]