# Dockerfile para Crypto Insight AI
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app/ ./app/
COPY run.py .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "run.py"]

