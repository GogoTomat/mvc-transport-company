FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends default-mysql-client gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pymysql==1.1.1

COPY . .
RUN chmod +x docker/backend/entrypoint.sh

EXPOSE 8000

CMD ["/app/docker/backend/entrypoint.sh"]
