FROM python:3.11-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    g++ \
    gcc \
    make \
    cmake \
    liblz4-dev \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
WORKDIR /app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]