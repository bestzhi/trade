FROM python:2.7.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN web pip install -r requirements.txt

EXPOSE 9000

CMD [ "python","app.py"]
