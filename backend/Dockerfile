FROM python:latest

WORKDIR /app

COPY requirements.txt .

# install system deps so we can use psql/pg_isready from the container
RUN apt-get update \
	&& apt-get install -y --no-install-recommends postgresql-client \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]