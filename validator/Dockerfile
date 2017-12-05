FROM python:alpine3.6
WORKDIR /usr/src/pmp_validator
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /usr/src/pmp_validator/validator
CMD [ "python", "./scheduler.py" ]