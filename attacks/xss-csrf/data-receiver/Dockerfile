FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

COPY .. .

RUN pip install --no-cache-dir Flask gunicorn

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
