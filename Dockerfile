FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY main_tron.py .
COPY run.py .

CMD ["python3", "run.py"]
