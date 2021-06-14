FROM python:3.8.0
MAINTAINER Ilya Soltanov <piccadillable@gmail.com>
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /aiohttp_vue_template/requirements.txt
WORKDIR /aiohttp_vue_template
RUN pip install -r requirements.txt
COPY . /aiohttp_vue_template
