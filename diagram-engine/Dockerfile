FROM python:latest
RUN apt-get update && apt-get install -y \
    graphviz \
    && apt-get clean

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app/

ENV HOST=${HOST}
ENV PORT=${PORT}

CMD ["python", "main.py"]
