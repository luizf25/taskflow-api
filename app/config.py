"""Configurações da aplicação lidas de variáveis de ambiente."""

import logging
import os

APP_NAME = "TaskFlow API"

# Versão da aplicação. Na imagem Docker ela é gravada no build pelo pipeline.
APP_VERSION = os.getenv("APP_VERSION", "dev")

# Nível de log: DEBUG, INFO, WARNING ou ERROR.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
