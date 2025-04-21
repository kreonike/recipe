FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && gunicorn --version \
    && python -c 'import psycopg2; print(psycopg2.__version__)' \
    && echo 'PATH: $PATH' \
    && ls -l /usr/local/bin/gunicorn

COPY . .

EXPOSE 8000

CMD ['gunicorn', '--bind', '0.0.0.0:8000', '--workers', '4', 'main:app']