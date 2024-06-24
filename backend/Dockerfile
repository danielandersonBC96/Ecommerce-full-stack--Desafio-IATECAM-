# backend/Dockerfile
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências especificadas no arquivo requirements.txt
RUN pip install -r requirements.txt

# Copia todo o código fonte da aplicação para o diretório de trabalho
COPY . .

# Instala o SQLite (caso não esteja presente na imagem base)
RUN apt-get update && apt-get install -y sqlite3

# Copia o arquivo do banco de dados SQLite para o diretório de trabalho do container
COPY db.sqlite /app/db.sqlite

# Comando para iniciar a aplicação utilizando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
