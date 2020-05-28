FROM python:3.8.2-alpine3.10 as base

WORKDIR /code

COPY requirements requirements

RUN echo https://mirrors.aliyun.com/alpine/v3.10/main > /etc/apk/repositories; \
    echo https://mirrors.aliyun.com/alpine/v3.10/community >> /etc/apk/repositories

RUN apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers tzdata;\
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime; \
    pip install --no-cache-dir -r requirements/common.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/; \
    apk del .build-deps;


FROM base as prod

RUN pip install --no-cache-dir -r requirements/prod.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY app app
COPY entrypoint.sh config.py manage.py ./
COPY migrations migrations

VOLUME ["/code/data"]

EXPOSE 5000
ENTRYPOINT tr -d '\r' < entrypoint.sh | sh