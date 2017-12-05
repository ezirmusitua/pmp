FROM python:3.6
WORKDIR /usr/src/pmp_spider
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /usr/src/pmp_spider/spider
CMD [ "python", "./scheduler.py" ]