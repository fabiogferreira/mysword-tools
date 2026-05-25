FROM python:3.11-slim

# Evitar gravacao de arquivos pyc e habilitar saida nao bufferizada
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

WORKDIR /app

# Instala dependencias nativas para compilacao caso necessario
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependencias do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o codigo-fonte da aplicacao
COPY src/ /app/src/

# Expoe a porta exigida pelo Hugging Face Spaces
EXPOSE 7860

# Comando para iniciar o servidor FastAPI
CMD ["python", "-m", "uvicorn", "src.web.app:app", "--host", "0.0.0.0", "--port", "7860"]
