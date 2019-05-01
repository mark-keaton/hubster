FROM python:3.7-alpine

RUN apk add build-base linux-headers

RUN mkdir -p /opt/services/hubster/src
WORKDIR /opt/services/hubster/src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /opt/services/hubster/src

EXPOSE 8000

CMD ["gunicorn", "--chdir", "hubster", "--bind", ":8000", "hubster.wsgi:application"]
