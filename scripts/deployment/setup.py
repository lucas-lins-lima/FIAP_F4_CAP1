import os
import sys
import subprocess
import shutil
from pathlib import Path

class FarmTechSetup:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.required_dirs = [
            'data', 'logs', 'models', 'backups',
            'assets/images/dashboard-screenshots',
            'assets/images/serial-plotter',
            'assets/images/system-demo'
        ]
        
    def create_directory_structure(self):
        """Cria estrutura de diretórios necessária"""
        print("📁 Criando estrutura de diretórios...")
        
        for directory in self.required_dirs:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {directory}")
        
        print("📁 Estrutura de diretórios criada com sucesso!")
    
    def install_python_dependencies(self):
        """Instala dependências Python"""
        print("🐍 Instalando dependências Python...")
        
        requirements_file = self.base_dir / "scripts" / "deployment" / "requirements.txt"
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
            print("✅ Dependências Python instaladas com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            return False
        
        return True
    
    def setup_database(self):
        """Configura banco de dados inicial"""
        print("🗄️ Configurando banco de dados...")
        
        try:
            sys.path.append(str(self.base_dir / "src" / "fase4" / "integration"))
            from database_enhanced import EnhancedFarmTechDatabase
            
            db = EnhancedFarmTechDatabase()
            print("✅ Banco de dados configurado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar banco de dados: {e}")
            return False
    
    def create_sample_data(self):
        """Cria dados de exemplo para demonstração"""
        print("📊 Criando dados de exemplo...")
        
        try:
            sys.path.append(str(self.base_dir / "src" / "fase4" / "integration"))
            from database_enhanced import EnhancedFarmTechDatabase
            import numpy as np
            from datetime import datetime, timedelta
            
            db = EnhancedFarmTechDatabase()
            
            # Gerar 200 registros de exemplo
            base_time = datetime.now() - timedelta(days=7)
            
            for i in range(200):
                timestamp = base_time + timedelta(minutes=i*30)
                hour = timestamp.hour
                
                # Padrões realistas
                humidity = max(15, min(85, 40 + 15 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 8)))
                ph = max(4.5, min(8.5, np.random.normal(6.7, 0.6)))
                phosphorus = np.random.choice([True, False], p=[0.7, 0.3])
                potassium = np.random.choice([True, False], p=[0.75, 0.25])
                pump_status = (humidity < 35) or (ph < 6.0 or ph > 7.5) or (not phosphorus or not potassium)
                temperature = 25 + 8 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 2)
                
                db.insert_enhanced_sensor_data(
                    humidity, ph, phosphorus, potassium, pump_status, temperature
                )
            
            print("✅ Dados de exemplo criados com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar dados de exemplo: {e}")
            return False
    
    def setup_ml_model(self):
        """Configura e treina modelo inicial de ML"""
        print("🤖 Configurando modelo de Machine Learning...")
        
        try:
            sys.path.append(str(self.base_dir / "src" / "fase4" / "machine_learning"))
            from model_training import ModelTrainer
            
            trainer = ModelTrainer()
            result = trainer.complete_training_pipeline()
            
            if result:
                print("✅ Modelo de ML configurado e treinado com sucesso!")
                return True
            else:
                print("⚠️ Modelo de ML configurado com avisos")
                return True
                
        except Exception as e:
            print(f"❌ Erro ao configurar modelo de ML: {e}")
            return False
    
    def create_env_file(self):
        """Cria arquivo .env com configurações padrão"""
        print("⚙️ Criando arquivo de configuração...")
        
        env_content = """# FarmTech Solutions - Configurações de Ambiente

# Banco de Dados
DB_PATH=data/farmtech_production.db
DB_BACKUP_PATH=backups/
DB_RETENTION_DAYS=90

# Sensores
SENSOR_HUMIDITY_MIN=30.0
SENSOR_HUMIDITY_MAX=70.0
SENSOR_PH_MIN=6.0
SENSOR_PH_MAX=7.5
SENSOR_READING_INTERVAL=300

# API Externa (OpenWeatherMap)
OPENWEATHER_API_KEY=YOUR_API_KEY_HERE
OPENWEATHER_CITY=São Paulo
OPENWEATHER_COUNTRY=BR

# Machine Learning
ML_MODEL_PATH=models/farmtech_irrigation_model.pkl
ML_RETRAIN_DAYS=7
ML_CONFIDENCE_THRESHOLD=0.7

# Sistema
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
LOG_FILE=logs/farmtech.log
"""
        
        env_file = self.base_dir / ".env"
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Arquivo .env criado!")
        print("⚠️ IMPORTANTE: Configure sua chave da API OpenWeather no arquivo .env")
    
    def run_setup(self):
        """Executa setup completo"""
        print("🚀 INICIANDO SETUP DO FARMTECH SOLUTIONS v4.0")
        print("=" * 50)
        
        steps = [
            ("Criar estrutura de diretórios", self.create_directory_structure),
            ("Instalar dependências Python", self.install_python_dependencies),
            ("Configurar banco de dados", self.setup_database),
            ("Criar dados de exemplo", self.create_sample_data),
            ("Configurar modelo ML", self.setup_ml_model),
            ("Criar arquivo de configuração", self.create_env_file)
        ]
        
        success_count = 0
        
        for step_name, step_function in steps:
            print(f"\n🔄 {step_name}...")
            try:
                if step_function():
                    success_count += 1
                    print(f"✅ {step_name} - CONCLUÍDO")
                else:
                    print(f"❌ {step_name} - FALHOU")
            except Exception as e:
                print(f"❌ {step_name} - ERRO: {e}")
        
        print("\n" + "=" * 50)
        print(f"📊 RESULTADO DO SETUP: {success_count}/{len(steps)} etapas concluídas")
        
        if success_count == len(steps):
            print("🎉 SETUP CONCLUÍDO COM SUCESSO!")
            print("\n📋 PRÓXIMOS PASSOS:")
            print("1. Configure sua chave da API OpenWeather no arquivo .env")
            print("2. Execute o dashboard: streamlit run src/fase4/dashboard/streamlit_app.py")
            print("3. Carregue o código ESP32 no Wokwi")
        else:
            print("⚠️ Setup incompleto. Verifique os erros acima.")
        
        return success_count == len(steps)

if __name__ == "__main__":
    setup = FarmTechSetup()
    setup.run_setup()