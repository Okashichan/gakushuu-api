FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM base as final

RUN mkdir -p /app/static/files
RUN mkdir -p /app/static/images

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]