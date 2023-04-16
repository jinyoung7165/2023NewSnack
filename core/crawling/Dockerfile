FROM public.ecr.aws/lambda/python as base

COPY .env ./
COPY remote ./remote

COPY crawling/requirements.txt  .
RUN pip install -r requirements.txt

COPY crawling/app.py ./
COPY crawling/crawl.py ./

# WORKDIR /tmp
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]