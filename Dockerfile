FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./req.txt ./
RUN pip install --no-cache-dir -r req.txt
RUN apt-get update && apt-get install -y ffmpeg \
    postgresql-client \ 
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

COPY scripts/migrate.sh /app/scripts/
RUN chmod +x /app/scripts/migrate.sh


ENTRYPOINT ["/app/scripts/migrate.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
