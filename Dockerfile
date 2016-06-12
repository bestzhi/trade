FROM python:3.4.3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 9000

CMD [ "python","app.py"]
