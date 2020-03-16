FROM python:3.7

RUN pip install sodapy

RUN pip install pandas

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


