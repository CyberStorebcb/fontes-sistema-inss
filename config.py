"""
Configurações do Sistema FONTES v3.0
Centralizador de configurações para ambiente de produção e desenvolvimento
"""
import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).parent.absolute()
SRC_DIR = BASE_DIR / "src"
DATABASE_DIR = BASE_DIR / "database"
LOGS_DIR = BASE_DIR / "logs"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Criar diretórios se não existirem
for directory in [DATABASE_DIR, LOGS_DIR, STATIC_DIR, TEMPLATES_DIR]:
    directory.mkdir(exist_ok=True)

# Configurações de ambiente
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
DEBUG = ENVIRONMENT == 'development'

# Configurações de segurança
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
SESSION_LIFETIME_DAYS = int(os.environ.get('SESSION_LIFETIME_DAYS', '30'))

# Configurações de banco de dados
DATABASE_PATH = DATABASE_DIR / "users.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configurações de servidor
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))

# Configurações de logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = LOGS_DIR / "app.log"

# Configurações de autenticação
MAX_LOGIN_ATTEMPTS = int(os.environ.get('MAX_LOGIN_ATTEMPTS', '999'))
LOCKOUT_DURATION_MINUTES = int(os.environ.get('LOCKOUT_DURATION_MINUTES', '0'))

# Configurações de aplicação
APP_NAME = "Sistema FONTES v3.0"
APP_VERSION = "3.0.0"
AUTHOR = "Sistema FONTES"

# URLs e endpoints
API_BASE_URL = "/api/v1"

class Config:
    """Classe de configuração base"""
    SECRET_KEY = SECRET_KEY
    DEBUG = DEBUG
    DATABASE_PATH = str(DATABASE_PATH)
    SESSION_LIFETIME_DAYS = SESSION_LIFETIME_DAYS
    MAX_LOGIN_ATTEMPTS = MAX_LOGIN_ATTEMPTS
    LOCKOUT_DURATION_MINUTES = LOCKOUT_DURATION_MINUTES

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Configuração ativa baseada no ambiente
if ENVIRONMENT == 'production':
    active_config = ProductionConfig
else:
    active_config = DevelopmentConfig
