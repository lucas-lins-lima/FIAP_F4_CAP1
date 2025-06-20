import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    """Configurações do banco de dados"""
    path: str = "farmtech_production.db"
    backup_path: str = "backups/"
    retention_days: int = 90
    max_connections: int = 10
    timeout: int = 30
    
    @classmethod
    def from_env(cls):
        """Carrega configurações das variáveis de ambiente"""
        return cls(
            path=os.getenv('DB_PATH', 'farmtech_production.db'),
            backup_path=os.getenv('DB_BACKUP_PATH', 'backups/'),
            retention_days=int(os.getenv('DB_RETENTION_DAYS', '90')),
            max_connections=int(os.getenv('DB_MAX_CONNECTIONS', '10')),
            timeout=int(os.getenv('DB_TIMEOUT', '30'))
        )

@dataclass
class SensorConfig:
    """Configurações dos sensores"""
    humidity_min: float = 30.0
    humidity_max: float = 70.0
    ph_min: float = 6.0
    ph_max: float = 7.5
    reading_interval: int = 300  # segundos
    alert_thresholds: dict = None
    
    def __post_init__(self):
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                'humidity_critical': 20.0,
                'humidity_warning': 25.0,
                'ph_critical_low': 5.0,
                'ph_critical_high': 8.5
            }
    
    @classmethod
    def from_env(cls):
        return cls(
            humidity_min=float(os.getenv('SENSOR_HUMIDITY_MIN', '30.0')),
            humidity_max=float(os.getenv('SENSOR_HUMIDITY_MAX', '70.0')),
            ph_min=float(os.getenv('SENSOR_PH_MIN', '6.0')),
            ph_max=float(os.getenv('SENSOR_PH_MAX', '7.5')),
            reading_interval=int(os.getenv('SENSOR_READING_INTERVAL', '300'))
        )

@dataclass
class APIConfig:
    """Configurações das APIs externas"""
    openweather_api_key: str = ""
    openweather_city: str = "São Paulo"
    openweather_country: str = "BR"
    update_interval: int = 3600  # segundos
    timeout: int = 10
    
    @classmethod
    def from_env(cls):
        return cls(
            openweather_api_key=os.getenv('OPENWEATHER_API_KEY', ''),
            openweather_city=os.getenv('OPENWEATHER_CITY', 'São Paulo'),
            openweather_country=os.getenv('OPENWEATHER_COUNTRY', 'BR'),
            update_interval=int(os.getenv('API_UPDATE_INTERVAL', '3600')),
            timeout=int(os.getenv('API_TIMEOUT', '10'))
        )

@dataclass
class MLConfig:
    """Configurações do Machine Learning"""
    model_path: str = "models/farmtech_irrigation_model.pkl"
    retrain_interval_days: int = 7
    min_training_samples: int = 100
    confidence_threshold: float = 0.7
    features: list = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = [
                'humidity', 'ph_level', 'phosphorus', 'potassium',
                'hour', 'temperature', 'weather_condition'
            ]
    
    @classmethod
    def from_env(cls):
        return cls(
            model_path=os.getenv('ML_MODEL_PATH', 'models/farmtech_irrigation_model.pkl'),
            retrain_interval_days=int(os.getenv('ML_RETRAIN_DAYS', '7')),
            min_training_samples=int(os.getenv('ML_MIN_SAMPLES', '100')),
            confidence_threshold=float(os.getenv('ML_CONFIDENCE_THRESHOLD', '0.7'))
        )

@dataclass
class SystemConfig:
    """Configurações gerais do sistema"""
    version: str = "4.0"
    debug: bool = False
    log_level: str = "INFO"
    log_file: str = "logs/farmtech.log"
    timezone: str = "America/Sao_Paulo"
    
    @classmethod
    def from_env(cls):
        return cls(
            version=os.getenv('SYSTEM_VERSION', '4.0'),
            debug=os.getenv('DEBUG', 'False').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            log_file=os.getenv('LOG_FILE', 'logs/farmtech.log'),
            timezone=os.getenv('TIMEZONE', 'America/Sao_Paulo')
        )

class ConfigManager:
    """Gerenciador central de configurações"""
    
    def __init__(self):
        self.database = DatabaseConfig.from_env()
        self.sensor = SensorConfig.from_env()
        self.api = APIConfig.from_env()
        self.ml = MLConfig.from_env()
        self.system = SystemConfig.from_env()
    
    def validate_config(self) -> dict:
        """Valida todas as configurações"""
        issues = []
        
        # Validar configurações do banco
        if not os.path.dirname(self.database.path):
            issues.append("Caminho do banco de dados inválido")
        
        # Validar configurações dos sensores
        if self.sensor.humidity_min >= self.sensor.humidity_max:
            issues.append("Limites de umidade inválidos")
        
        if self.sensor.ph_min >= self.sensor.ph_max:
            issues.append("Limites de pH inválidos")
        
        # Validar API
        if not self.api.openweather_api_key:
            issues.append("Chave da API OpenWeather não configurada")
        
        # Validar ML
        if not os.path.exists(os.path.dirname(self.ml.model_path)):
            issues.append("Diretório do modelo ML não existe")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def create_directories(self):
        """Cria diretórios necessários"""
        directories = [
            os.path.dirname(self.database.path),
            self.database.backup_path,
            os.path.dirname(self.ml.model_path),
            os.path.dirname(self.system.log_file)
        ]
        
        for directory in directories:
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                print(f"📁 Diretório criado: {directory}")
    
    def export_config(self, filepath: str = "config/current_config.json"):
        """Exporta configurações atuais para arquivo"""
        import json
        from dataclasses import asdict
        
        config_dict = {
            'database': asdict(self.database),
            'sensor': asdict(self.sensor),
            'api': asdict(self.api),
            'ml': asdict(self.ml),
            'system': asdict(self.system)
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        print(f"⚙️ Configurações exportadas para: {filepath}")

# Instância global
config = ConfigManager()