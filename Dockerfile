FROM python:3.13-slim

# Versão da aplicação, informada pelo pipeline no momento do build
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala apenas as dependências de execução (sem ferramentas de teste)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Executa a aplicação com um usuário sem privilégios de root
RUN useradd --no-create-home --shell /usr/sbin/nologin appuser
USER appuser

EXPOSE 8000

# Docker marca o container como "unhealthy" se o /health parar de responder
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
