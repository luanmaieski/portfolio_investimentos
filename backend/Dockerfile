FROM python:3.13

WORKDIR /app

# Copia só o requirements primeiro (para cache de dependências)
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todo o código do backend para /app
COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
