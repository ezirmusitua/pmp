FROM python:alpine3.6
WORKDIR /usr/src/pmp_server
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /usr/src/pmp_server/server
CMD [ "python", "./run.py" ]