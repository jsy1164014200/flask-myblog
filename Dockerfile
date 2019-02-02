FROM python:3
MAINTAINER Jason Jiang <gng@bingyan.net>

COPY . /project/
WORKDIR /project
RUN pip install -r requirements.txt && chmod +x scripts/dev.sh
