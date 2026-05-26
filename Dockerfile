FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/

ARG REQUIREMENTS=development
RUN pip install --upgrade pip && pip install -r requirements/${REQUIREMENTS}.txt

COPY . .

RUN mkdir -p staticfiles

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]