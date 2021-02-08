# --- Base Image
FROM python:3.8-slim

# --- Copy requirements file
COPY requirements.txt .

# --- Install python packages
# libpq-dev and gcc are a psycopg2 dependency;
# libffi-dev python-dev and gcc are dependencies for bcrypt.
RUN apt-get clean && \
    apt-get -y update && \
    apt-get install -y \
    libpq-dev \
    libffi-dev \
    python-dev \
    libpcre3 \
    libpcre3-dev \
    gcc \
    && pip3 install -r requirements.txt --no-cache-dir \
    && apt-get autoremove -y gcc

# --- Copy application files
COPY . .

# --- Set Flask server variables
ENV FLASK_PORT=5000
ENV FLASK_HOST=0.0.0.0
ENV FLASK_DEBUG=True

# --- Document exposed port
EXPOSE 5000

# --- Run uWSGI
CMD ["uwsgi", "--ini", "/wsgi.ini"]
