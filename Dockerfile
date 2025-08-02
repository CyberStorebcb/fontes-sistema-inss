# Sistema FONTES v3.0 - Dockerfile
FROM python:3.11-slim

# Metadados
LABEL maintainer="Sistema FONTES <admin@fontes.inss.gov.br>"
LABEL version="3.0"
LABEL description="Sistema FONTES - Aplicação Web para INSS"

# Configurar timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd -m -u 1000 fontes && \
    mkdir -p /app && \
    chown -R fontes:fontes /app

# Configurar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (cache Docker)
COPY requirements-prod.txt requirements.txt

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY --chown=fontes:fontes . .

# Alterar para usuário não-root
USER fontes

# Configurar variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/data && chown -R fontes:fontes /app

# Expor porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Comando padrão com gunicorn para produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
