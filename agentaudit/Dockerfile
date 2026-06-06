# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agentaudit/ ./agentaudit/
COPY http_server.py .

EXPOSE 8000

CMD ["python", "http_server.py"]
