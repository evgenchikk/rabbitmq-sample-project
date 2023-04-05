FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY . /app

RUN pip install --no-cache -r requirements.txt

ENTRYPOINT ["python", "main.py"]
