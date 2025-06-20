import os
from pathlib import Path

# Caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "models" 
BACKUPS_DIR = BASE_DIR / "backups"

# Configurações de desenvolvimento vs produção
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = ENVIRONMENT == 'development'

# Configurações do banco de dados
DATABASE_CONFIG = {
    'development': {
        'path': str(DATA_DIR / "farmtech_dev.db"),
        'backup_enabled': False
    },
    'production': {
        'path': str(DATA_DIR / "farmtech_prod.db"),
        'backup_enabled': True,
        'backup_interval_hours': 6
    }
}

# Configurações de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'farmtech.log'),
            'formatter': 'detailed',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'farmtech': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    'page_title': 'FarmTech Solutions v4.0',
    'page_icon': '🌾',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'menu_items': {
        'Get Help': 'https://github.com/farmtech-solutions/docs',
        'Report a bug': 'https://github.com/farmtech-solutions/issues',
        'About': "FarmTech Solutions v4.0 - Sistema de Agricultura Digital"
    }
}

# Criar diretórios necessários
for directory in [DATA_DIR, LOGS_DIR, MODELS_DIR, BACKUPS_DIR]:
    directory.mkdir(exist_ok=True)