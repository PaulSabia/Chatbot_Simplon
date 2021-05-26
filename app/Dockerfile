FROM python:3.8-slim-buster

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python -m nltk.downloader stopwords

