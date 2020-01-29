FROM python:3.7

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /srv

ADD . /srv

ENV FLASK_ENV=production
ENV DATA_FOLDER=./data
ENV DB_NAME=db.sqlite

CMD ["uwsgi", "--ini", "myuri.ini"]
