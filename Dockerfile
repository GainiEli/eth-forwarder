FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY main_tron.py .
COPY main_optimism.py .
COPY main_bnb.py .
COPY main_solana.py .
COPY run.py .

CMD ["python3", "run.py"]
