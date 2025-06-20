import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedFarmTechDatabase:
    def __init__(self, db_path: str = "farmtech_enhanced.db"):
        self.db_path = db_path
        self.init_enhanced_database()
    
    def init_enhanced_database(self):
        """Inicializa banco de dados aprimorado com novas tabelas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela principal de sensores (aprimorada)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                humidity REAL NOT NULL,
                ph_level REAL NOT NULL,
                phosphorus BOOLEAN NOT NULL,
                potassium BOOLEAN NOT NULL,
                pump_status BOOLEAN NOT NULL,
                location TEXT DEFAULT 'Campo_Principal',
                temperature REAL,
                light_intensity REAL,
                soil_conductivity REAL,
                weather_condition TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de predições ML
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ml_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sensor_reading_id INTEGER,
                predicted_irrigation BOOLEAN NOT NULL,
                confidence_score REAL NOT NULL,
                model_version TEXT,
                features_used TEXT,
                actual_irrigation BOOLEAN,
                prediction_accuracy REAL,
                FOREIGN KEY (sensor_reading_id) REFERENCES sensor_readings (id)
            )
        ''')
        
        # Tabela de configurações do sistema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parameter_name TEXT UNIQUE NOT NULL,
                parameter_value TEXT NOT NULL,
                parameter_type TEXT DEFAULT 'string',
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_by TEXT DEFAULT 'system'
            )
        ''')
        
        # Tabela de alertas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                sensor_reading_id INTEGER,
                acknowledged BOOLEAN DEFAULT FALSE,
                acknowledged_at DATETIME,
                acknowledged_by TEXT,
                FOREIGN KEY (sensor_reading_id) REFERENCES sensor_readings (id)
            )
        ''')
        
        # Tabela de histórico de irrigação
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS irrigation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                duration_minutes INTEGER,
                water_amount_liters REAL,
                trigger_reason TEXT,
                efficiency_score REAL,
                cost_estimate REAL,
                location TEXT DEFAULT 'Campo_Principal'
            )
        ''')
        
        # Tabela de dados meteorológicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature REAL,
                humidity REAL,
                pressure REAL,
                wind_speed REAL,
                precipitation REAL,
                weather_condition TEXT,
                forecast_hours INTEGER DEFAULT 0,
                data_source TEXT
            )
        ''')
        
        # Índices para performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sensor_timestamp ON sensor_readings(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON system_alerts(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_irrigation_start ON irrigation_history(start_time)')
        
        # Inserir configurações padrão
        self.insert_default_config(cursor)
        
        conn.commit()
        conn.close()
        logger.info("✅ Banco de dados aprimorado inicializado com sucesso!")
    
    def insert_default_config(self, cursor):
        """Insere configurações padrão do sistema"""
        default_configs = [
            ('humidity_min_threshold', '30.0', 'float', 'Limite mínimo de umidade para irrigação'),
            ('humidity_max_threshold', '70.0', 'float', 'Limite máximo de umidade'),
            ('ph_min_threshold', '6.0', 'float', 'pH mínimo ideal'),
            ('ph_max_threshold', '7.5', 'float', 'pH máximo ideal'),
            ('irrigation_duration_default', '15', 'int', 'Duração padrão de irrigação em minutos'),
            ('alert_email_enabled', 'true', 'bool', 'Envio de alertas por email'),
            ('ml_prediction_enabled', 'true', 'bool', 'Usar predições de ML'),
            ('data_retention_days', '90', 'int', 'Dias para manter dados históricos'),
            ('system_version', '4.0', 'string', 'Versão do sistema FarmTech')
        ]
        
        for config in default_configs:
            cursor.execute('''
                INSERT OR IGNORE INTO system_config 
                (parameter_name, parameter_value, parameter_type, description)
                VALUES (?, ?, ?, ?)
            ''', config)
    
    def insert_enhanced_sensor_data(self, humidity: float, ph_level: float, 
                                  phosphorus: bool, potassium: bool, pump_status: bool,
                                  temperature: float = None, light_intensity: float = None,
                                  soil_conductivity: float = None, weather_condition: str = None,
                                  location: str = 'Campo_Principal') -> int:
        """Insere dados dos sensores com informações aprimoradas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_readings 
            (humidity, ph_level, phosphorus, potassium, pump_status, 
             temperature, light_intensity, soil_conductivity, weather_condition, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (humidity, ph_level, phosphorus, potassium, pump_status,
              temperature, light_intensity, soil_conductivity, weather_condition, location))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Verificar se precisa gerar alertas
        self.check_and_create_alerts(record_id, humidity, ph_level, phosphorus, potassium)
        
        return record_id
    
    def insert_ml_prediction(self, sensor_reading_id: int, predicted_irrigation: bool,
                           confidence_score: float, model_version: str,
                           features_used: List[str]) -> int:
        """Insere predição de ML"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        features_json = json.dumps(features_used)
        
        cursor.execute('''
            INSERT INTO ml_predictions 
            (sensor_reading_id, predicted_irrigation, confidence_score, 
             model_version, features_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (sensor_reading_id, predicted_irrigation, confidence_score,
              model_version, features_json))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return prediction_id
    
    def check_and_create_alerts(self, sensor_reading_id: int, humidity: float,
                              ph_level: float, phosphorus: bool, potassium: bool):
        """Verifica condições e cria alertas automaticamente"""
        alerts = []
        
        # Verificar umidade crítica
        if humidity < 20:
            alerts.append(('CRITICAL', 'HUMIDITY', f'Umidade crítica: {humidity:.1f}%'))
        elif humidity < 30:
            alerts.append(('WARNING', 'HUMIDITY', f'Umidade baixa: {humidity:.1f}%'))
        
        # Verificar pH
        if ph_level < 5.5 or ph_level > 8.0:
            alerts.append(('WARNING', 'PH', f'pH fora da faixa ideal: {ph_level:.2f}'))
        
        # Verificar nutrientes
        if not phosphorus:
            alerts.append(('INFO', 'NUTRIENT', 'Fósforo insuficiente detectado'))
        
        if not potassium:
            alerts.append(('INFO', 'NUTRIENT', 'Potássio insuficiente detectado'))
        
        # Inserir alertas
        if alerts:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for severity, alert_type, message in alerts:
                cursor.execute('''
                    INSERT INTO system_alerts 
                    (alert_type, severity, message, sensor_reading_id)
                    VALUES (?, ?, ?, ?)
                ''', (alert_type, severity, message, sensor_reading_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"🚨 {len(alerts)} alerta(s) criado(s) para leitura {sensor_reading_id}")
    
    def get_recent_alerts(self, hours: int = 24, acknowledged: bool = False) -> List[Dict]:
        """Retorna alertas recentes"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM system_alerts 
            WHERE timestamp >= datetime('now', '-{} hours')
            AND acknowledged = ?
            ORDER BY timestamp DESC
        '''.format(hours), (acknowledged,))
        
        alerts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return alerts
    
    def acknowledge_alert(self, alert_id: int, acknowledged_by: str = 'user') -> bool:
        """Marca alerta como reconhecido"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE system_alerts 
            SET acknowledged = TRUE, 
                acknowledged_at = CURRENT_TIMESTAMP,
                acknowledged_by = ?
            WHERE id = ?
        ''', (acknowledged_by, alert_id))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def get_enhanced_statistics(self, days: int = 7) -> Dict:
        """Retorna estatísticas aprimoradas do sistema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Estatísticas básicas dos sensores
        cursor.execute('''
            SELECT 
                COUNT(*) as total_readings,
                AVG(humidity) as avg_humidity,
                MIN(humidity) as min_humidity,
                MAX(humidity) as max_humidity,
                AVG(ph_level) as avg_ph,
                MIN(ph_level) as min_ph,
                MAX(ph_level) as max_ph,
                SUM(CASE WHEN pump_status = 1 THEN 1 ELSE 0 END) as pump_activations,
                AVG(temperature) as avg_temperature
            FROM sensor_readings
            WHERE timestamp >= datetime('now', '-{} days')
        '''.format(days))
        
        basic_stats = cursor.fetchone()
        
        # Estatísticas de alertas
        cursor.execute('''
            SELECT 
                COUNT(*) as total_alerts,
                COUNT(CASE WHEN severity = 'CRITICAL' THEN 1 END) as critical_alerts,
                COUNT(CASE WHEN severity = 'WARNING' THEN 1 END) as warning_alerts,
                COUNT(CASE WHEN acknowledged = 1 THEN 1 END) as acknowledged_alerts
            FROM system_alerts
            WHERE timestamp >= datetime('now', '-{} days')
        '''.format(days))
        
        alert_stats = cursor.fetchone()
        
        # Estatísticas de irrigação
        cursor.execute('''
            SELECT 
                COUNT(*) as irrigation_sessions,
                AVG(duration_minutes) as avg_duration,
                SUM(water_amount_liters) as total_water_used,
                AVG(efficiency_score) as avg_efficiency
            FROM irrigation_history
            WHERE start_time >= datetime('now', '-{} days')
        '''.format(days))
        
        irrigation_stats = cursor.fetchone()
        
        # Estatísticas de ML
        cursor.execute('''
            SELECT 
                COUNT(*) as total_predictions,
                AVG(confidence_score) as avg_confidence,
                AVG(prediction_accuracy) as avg_accuracy
            FROM ml_predictions
            WHERE timestamp >= datetime('now', '-{} days')
        '''.format(days))
        
        ml_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'period_days': days,
            'sensor_stats': dict(basic_stats) if basic_stats else {},
            'alert_stats': dict(alert_stats) if alert_stats else {},
            'irrigation_stats': dict(irrigation_stats) if irrigation_stats else {},
            'ml_stats': dict(ml_stats) if ml_stats else {},
            'generated_at': datetime.now().isoformat()
        }
    
    def cleanup_old_data(self, retention_days: int = 90):
        """Remove dados antigos baseado na política de retenção"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tables_to_clean = [
            'sensor_readings',
            'ml_predictions',
            'system_alerts',
            'weather_data'
        ]
        
        total_deleted = 0
        
        for table in tables_to_clean:
            cursor.execute(f'''
                DELETE FROM {table}
                WHERE timestamp < datetime('now', '-{retention_days} days')
            ''')
            deleted = cursor.rowcount
            total_deleted += deleted
            logger.info(f"🗑️ Removidos {deleted} registros antigos de {table}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Limpeza concluída: {total_deleted} registros removidos")
        return total_deleted
    
    def export_data_to_csv(self, table_name: str, days: int = 30, 
                          filepath: str = None) -> str:
        """Exporta dados para CSV"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"farmtech_{table_name}_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        
        query = f'''
            SELECT * FROM {table_name}
            WHERE timestamp >= datetime('now', '-{days} days')
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        df.to_csv(filepath, index=False)
        
        conn.close()
        
        logger.info(f"📊 Dados exportados para: {filepath}")
        return filepath
    
    def get_system_health(self) -> Dict:
        """Retorna status de saúde do sistema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar últimas leituras
        cursor.execute('''
            SELECT timestamp FROM sensor_readings 
            ORDER BY timestamp DESC LIMIT 1
        ''')
        last_reading = cursor.fetchone()
        
        # Verificar alertas críticos não reconhecidos
        cursor.execute('''
            SELECT COUNT(*) FROM system_alerts 
            WHERE severity = 'CRITICAL' AND acknowledged = FALSE
        ''')
        critical_alerts = cursor.fetchone()[0]
        
        # Verificar taxa de erro das predições ML
        cursor.execute('''
            SELECT AVG(prediction_accuracy) FROM ml_predictions 
            WHERE timestamp >= datetime('now', '-24 hours')
            AND prediction_accuracy IS NOT NULL
        ''')
        ml_accuracy = cursor.fetchone()[0]
        
        conn.close()
        
        # Calcular score de saúde
        health_score = 100
        
        if last_reading:
            last_time = datetime.fromisoformat(last_reading[0].replace('Z', '+00:00'))
            time_diff = datetime.now() - last_time
            if time_diff > timedelta(hours=1):
                health_score -= 30
        else:
            health_score -= 50
        
        if critical_alerts > 0:
            health_score -= (critical_alerts * 20)
        
        if ml_accuracy and ml_accuracy < 0.8:
            health_score -= 15
        
        health_score = max(0, health_score)
        
        # Determinar status
        if health_score >= 90:
            status = "EXCELLENT"
            status_emoji = "🟢"
        elif health_score >= 70:
            status = "GOOD"
            status_emoji = "🟡"
        elif health_score >= 50:
            status = "WARNING"
            status_emoji = "🟠"
        else:
            status = "CRITICAL"
            status_emoji = "🔴"
        
        return {
            'health_score': health_score,
            'status': status,
            'status_emoji': status_emoji,
            'last_reading': last_reading[0] if last_reading else None,
            'critical_alerts': critical_alerts,
            'ml_accuracy': ml_accuracy,
            'checked_at': datetime.now().isoformat()
        }

# Exemplo de uso
if __name__ == "__main__":
    db = EnhancedFarmTechDatabase()
    
    # Inserir dados de exemplo
    for i in range(10):
        humidity = np.random.uniform(25, 65)
        ph = np.random.uniform(5.5, 8.0)
        phosphorus = np.random.choice([True, False], p=[0.7, 0.3])
        potassium = np.random.choice([True, False], p=[0.75, 0.25])
        pump_status = humidity < 35 or ph < 6.0 or ph > 7.5
        temperature = np.random.uniform(20, 35)
        
        record_id = db.insert_enhanced_sensor_data(
            humidity, ph, phosphorus, potassium, pump_status, temperature
        )
        print(f"📊 Registro {record_id} inserido")
    
    # Mostrar estatísticas
    stats = db.get_enhanced_statistics()
    print(f"\n📈 Estatísticas: {stats}")
    
    # Mostrar saúde do sistema
    health = db.get_system_health()
    print(f"\n{health['status_emoji']} Saúde do sistema: {health['status']} ({health['health_score']}%)")