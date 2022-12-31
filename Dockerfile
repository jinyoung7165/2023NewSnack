FROM public.ecr.aws/lambda/python:3.8 as lambda-image
FROM ubuntu:20.04 as build
ARG DEBIAN_FRONTEND=noninteractive

#------------------python 및 빌드 종속성 설치------------------#
RUN apt-get -y update && apt install -y unzip && apt install -y libgl1-mesa-glx libglib2.0-0 && \
    apt install python3 -y --no-install-recommends && \
    apt install python3-pip -y --no-install-recommends && \
    apt install -y python3-dev && apt install -y unzip
#------------------------------------------------------------#

#------------Lambda Runtime Interface Emulator 추가--------------#
# ENTRYPOINT에서 스크립트 사용을 통해 간단한 로컬 사용 지원
COPY ./entry_script.sh /entry_script.sh
ADD aws-lambda-rie /usr/local/bin/aws-lambda-rie

RUN chmod 755 /entry_script.sh
RUN chmod 755 /usr/local/bin/aws-lambda-rie

ENTRYPOINT [ "/entry_script.sh" ]
#------------------------------------------------------------#

#------------------작업 디렉토리 설정------------------#
RUN mkdir /var/task
WORKDIR /var/task
#--------------------------------------------------#

RUN pip install awslambdaric && \
    pip install boto3

#------------------labmda 런타임 이미지 복사------------------#
COPY app.py /var/task/
COPY --from=lambda-image /var/runtime /var/runtime
#---------------------------------------------------------#

COPY app.py /var/task/

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "/var/task"

RUN apt-get -y update && apt install -y curl

RUN curl -Lo "chromedriver.zip" "https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip"
RUN curl -Lo "chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1058929%2Fchrome-linux.zip?alt=media"
    
RUN  unzip chromedriver.zip -d /var/task/chromedriver
RUN  unzip chrome-linux.zip -d /var/task/chrome-linux 

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]