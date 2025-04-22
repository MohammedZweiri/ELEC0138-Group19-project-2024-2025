FROM --platform=linux/amd64 python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY .. .

RUN pip install --no-cache-dir Flask gunicorn
RUN pip install --no-cache-dir flask-cors flask-jwt-extended flask-mysqldb flask-smorest python-dotenv requests

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "backend:app"]
