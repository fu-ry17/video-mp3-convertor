FROM python:3.12-slim

RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "5000"]
