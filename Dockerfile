# --- Base Image
FROM vmpereiraf/gdal-py:latest

# --- Copy application files
COPY . .

# --- Set Flask server variables
ENV FLASK_PORT=8080
ENV FLASK_HOST=0.0.0.0
ENV FLASK_DEBUG=False
ENV FLASK_KEY=_6ZPJgtzFHMSlxcl609RryDmHO35g7Yd4xEyySJLK_s=

# --- Document exposed port
EXPOSE 8080

# --- Run uWSGI
CMD ["uwsgi", "--ini", "/wsgi.ini"]