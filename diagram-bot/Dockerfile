FROM python:latest

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app/

ENV TELEGRAM_API_TOKEN=${TELEGRAM_API_TOKEN}
ENV API_URL=${API_URL}

CMD ["python", "main.py"]
