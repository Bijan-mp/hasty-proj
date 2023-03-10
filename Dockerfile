FROM python:3.8

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONPATH=/app/src

COPY . .
