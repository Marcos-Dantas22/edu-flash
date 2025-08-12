# construir um dockerfile para iniciar o servidor do backend e rodar os pacotes
# saber como e a estrutura base de um projeto fast api com parte de configuração e utilizando env
# conectar ao banco de dados no Neon Serverless Postgres

FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]