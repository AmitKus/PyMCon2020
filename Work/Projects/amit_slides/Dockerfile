# create ubuntu image with git, and pandoc
# docker build -t pelican-base .

FROM ubuntu:20.04
# ARG DEBIAN_FRONTEND=noninteractive
MAINTAINER Jerry Asher <ja2038@gmail.com>
# RUN apt-get update
# RUN apt-get install -y apt-utils
# RUN apt-get install -y python-pip python-dev build-essential
# RUN pip install --upgrade pip
RUN \
  apt-get update && \
#  apt-get install -y apt-utils && \
  apt-get install -y python3-pip python3-dev && \
  cd /usr/local/bin && \
  ln -s /usr/bin/python3 python && \
  pip3 install --upgrade pip
RUN apt-get install -y git
RUN apt-get install -y pandoc

