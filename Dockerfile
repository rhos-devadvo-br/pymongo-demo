FROM python:3-slim

WORKDIR /usr/app

COPY . .

RUN apt-get clean && \
    apt-get -y update && \
    apt-get install -y build-essential && \
    pip install -r requirements.txt

ENV DATABASE_NAME=A
ENV DATABASE_USER=B
ENV DATABASE_PASSWORD=C

EXPOSE 8080

# CMD ["python", "app.py"]
CMD ["uwsgi", "--ini", "wsgi.ini"]