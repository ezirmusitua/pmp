FROM python:3.6
ADD . /self_proxy_list
WORKDIR /self_proxy_list
RUN pip install -r requirements.txt
