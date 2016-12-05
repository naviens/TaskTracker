# Build Django server Docker container
FROM python:2.7
ENV PYTHONUNBUFFERED 1
ARG APP_ROOT=/webapps/rest_app

# postgres client
RUN apt-get -y update
RUN apt-get -y install postgresql-client

RUN mkdir -p $APP_ROOT/logs
ADD ./requirements.txt $APP_ROOT
WORKDIR $APP_ROOT
RUN pip install -r requirements.txt

ADD sbin $APP_ROOT/sbin
RUN chmod 755 sbin/*.sh
ADD conf $APP_ROOT/conf

ADD src $APP_ROOT/src
