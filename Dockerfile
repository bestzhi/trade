FROM python:2.7.8

RUN apt-get update && \
    apt-get install -y python \
                       python-dev \
                       python-pip 
                       
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 9000

CMD [ "python","app.py"]