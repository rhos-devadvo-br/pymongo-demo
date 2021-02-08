# --- Base Image
FROM python:3.8-slim

# --- Copy requirements file
COPY requirements.txt .

# --- Install python packages
# libpq-dev and gcc are a psycopg2 dependency;
# libffi-dev python-dev and gcc are dependencies for bcrypt.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=10.1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt --no-cache-dir

# --- Copy application files
COPY . .

# --- Set Flask server variables
ENV FLASK_PORT=8080
ENV FLASK_HOST=0.0.0.0
ENV FLASK_DEBUG=True

# --- Document exposed port
EXPOSE 8080

# --- Run uWSGI
CMD ["uwsgi", "--ini", "/wsgi.ini"]
