FROM python:3

# apt init
ENV LANG=C.UTF-8
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata g++ git curl cron

# timezone
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy cron file to the cron.d directory on container
COPY test/cron /etc/cron.d/cron
# Give execution access
RUN chmod 0755 /etc/cron.d/cron
# Run cron job on cron file
RUN crontab /etc/cron.d/cron
# Create the log file
RUN touch /var/log/cron.log

# app 디렉토리 생성
RUN mkdir -p /app

#RUN, CMD, ENTRYPOINT의 명령이 실행될 디렉터리
WORKDIR /app

COPY test/requirements.txt  ./
RUN pip install -r requirements.txt

COPY test/t.py ./

# container 종료 막음
CMD tail -f /dev/null