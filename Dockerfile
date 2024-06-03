FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get install -y certbot && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/static/files /app/static/images

COPY /etc/letsencrypt/live/gakushuu.pp.ua/privkey.pem /etc/letsencrypt/live/gakushuu.pp.ua/privkey.pem
COPY /etc/letsencrypt/live/gakushuu.pp.ua/fullchain.pem /etc/letsencrypt/live/gakushuu.pp.ua/fullchain.pem

FROM base as final

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "/etc/letsencrypt/live/gakushuu.pp.ua/privkey.pem", "--ssl-certfile", "/etc/letsencrypt/live/gakushuu.pp.ua/fullchain.pem"]