FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY wsgi.py wsgi.py
RUN pip3 install -r requirements.txt
CMD ["gunicorn","--bind","0.0.0.0:5000","wsgi:app"]