FROM python:3.10.2-slim-buster

ENV PATH=/root/.local/bin:$PATH

WORKDIR /root

COPY requirements /root/requirements

RUN pip3 install --no-cache-dir -U pip && \
    pip3 install --no-cache-dir -U -r /root/requirements/base.txt && \
    rm -r /root/requirements

COPY bot /root/bot

CMD
