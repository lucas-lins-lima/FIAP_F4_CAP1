import sqlite3
import datetime
from typing import List, Dict, Optional

class FarmTechDatabase:
    def __init__(self, db_path: str = "farmtech_sensors.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela para dados dos sensores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                humidity REAL NOT NULL,
                ph_level REAL NOT NULL,
                phosphorus BOOLEAN NOT NULL,
                potassium BOOLEAN NOT NULL,
                pump_status BOOLEAN NOT NULL,
                location TEXT DEFAULT 'Campo_Principal'
            )
        ''')
        
        # Tabela para histórico de irrigação
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS irrigation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                action TEXT NOT NULL,
                reason TEXT,
                duration_minutes INTEGER,
                water_amount_liters REAL
            )
        ''')
        
        # Tabela para configurações do sistema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parameter_name TEXT UNIQUE NOT NULL,
                parameter_value TEXT NOT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
    
    def insert_sensor_data(self, humidity: float, ph: float, 
                          phosphorus: bool, potassium: bool, pump_status: bool) -> int:
        """Insere dados dos sensores no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_readings 
            (humidity, ph_level, phosphorus, potassium, pump_status)
            VALUES (?, ?, ?, ?, ?)
        ''', (humidity, ph, phosphorus, potassium, pump_status))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_sensor_data(self, limit: int = 100) -> List[Dict]:
        """Recupera dados dos sensores"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sensor_readings 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_sensor_data(self, record_id: int, **kwargs) -> bool:
        """Atualiza dados de um registro específico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Construir query dinâmica
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [record_id]
        
        cursor.execute(f'''
            UPDATE sensor_readings 
            SET {set_clause}
            WHERE id = ?
        ''', values)
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def delete_sensor_data(self, record_id: int) -> bool:
        """Remove um registro específico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sensor_readings WHERE id = ?', (record_id,))
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def get_statistics(self) -> Dict:
        """Calcula estatísticas dos dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_readings,
                AVG(humidity) as avg_humidity,
                MIN(humidity) as min_humidity,
                MAX(humidity) as max_humidity,
                AVG(ph_level) as avg_ph,
                MIN(ph_level) as min_ph,
                MAX(ph_level) as max_ph,
                SUM(CASE WHEN pump_status = 1 THEN 1 ELSE 0 END) as pump_activations
            FROM sensor_readings
        ''')
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            'total_readings': stats[0] or 0,
            'avg_humidity': round(stats[1] or 0, 2),
            'min_humidity': stats[2] or 0,
            'max_humidity': stats[3] or 0,
            'avg_ph': round(stats[4] or 0, 2),
            'min_ph': stats[5] or 0,
            'max_ph': stats[6] or 0,
            'pump_activations': stats[7] or 0
        }

# Exemplo de uso
if __name__ == "__main__":
    db = FarmTechDatabase()
    
    # Dados de exemplo (simulando dados do ESP32)
    sample_data = [
        (45.2, 6.8, True, True, False),
        (32.1, 7.2, False, True, True),
        (28.5, 5.9, True, False, True),
        (51.3, 7.0, True, True, False),
        (35.7, 6.5, False, False, True)
    ]
    
    # Inserir dados de exemplo
    for humidity, ph, phos, pot, pump in sample_data:
        record_id = db.insert_sensor_data(humidity, ph, phos, pot, pump)
        print(f"📊 Registro {record_id} inserido: H={humidity}%, pH={ph}")
    
    # Mostrar estatísticas
    stats = db.get_statistics()
    print("\n📈 Estatísticas do Sistema:")
    for key, value in stats.items():
        print(f"  {key}: {value}")