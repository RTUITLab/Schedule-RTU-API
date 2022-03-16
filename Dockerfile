FROM tiangolo/uvicorn-gunicorn:python3.9-slim

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .