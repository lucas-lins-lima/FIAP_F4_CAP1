import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from datetime import datetime, timedelta
import sqlite3
import sys
import os

# Adicionar o caminho para importar database_manager
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/fase3/python'))
from database_manager import FarmTechDatabase

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')
        self.label_encoder = LabelEncoder()
        
    def load_sensor_data(self, limit=1000):
        """Carrega dados dos sensores do banco de dados"""
        print("📊 Carregando dados dos sensores...")
        
        db = FarmTechDatabase()
        data = db.get_sensor_data(limit)
        
        if not data:
            print("⚠️ Nenhum dado encontrado! Gerando dados de exemplo...")
            return self.generate_sample_data()
        
        df = pd.DataFrame(data)
        print(f"✅ Carregados {len(df)} registros do banco de dados")
        return df
    
    def generate_sample_data(self, n_samples=1000):
        """Gera dados de exemplo para desenvolvimento"""
        print(f"🔄 Gerando {n_samples} amostras de exemplo...")
        
        np.random.seed(42)
        data = []
        
        base_time = datetime.now() - timedelta(days=30)
        
        for i in range(n_samples):
            # Timestamp incremental
            timestamp = base_time + timedelta(minutes=i*15)
            hour = timestamp.hour
            day_of_week = timestamp.weekday()
            
            # Padrões realistas baseados no horário
            if 6 <= hour <= 18:  # Período diurno
                base_humidity = 35 + 10 * np.sin(2 * np.pi * hour / 24)
                temp_factor = 1.2
            else:  # Período noturno
                base_humidity = 55 + 5 * np.sin(2 * np.pi * hour / 24)
                temp_factor = 0.8
            
            humidity = max(15, min(85, np.random.normal(base_humidity, 8)))
            ph_level = np.random.normal(6.7, 0.6)
            ph_level = max(4.5, min(8.5, ph_level))
            
            # Nutrientes com padrões sazonais
            phosphorus = np.random.choice([0, 1], p=[0.25, 0.75])
            potassium = np.random.choice([0, 1], p=[0.3, 0.7])
            
            # Lógica de irrigação complexa
            irrigation_needed = (
                (humidity < 30) or
                (humidity < 40 and (ph_level < 6.0 or ph_level > 7.5)) or
                (phosphorus == 0 or potassium == 0) or
                (hour >= 6 and hour <= 10 and humidity < 45) or  # Irrigação matinal
                (hour >= 16 and hour <= 18 and humidity < 40)   # Irrigação vespertina
            )
            
            data.append({
                'id': i + 1,
                'timestamp': timestamp.isoformat(),
                'humidity': round(humidity, 2),
                'ph_level': round(ph_level, 2),
                'phosphorus': phosphorus,
                'potassium': potassium,
                'pump_status': int(irrigation_needed),
                'hour': hour,
                'day_of_week': day_of_week,
                'temperature': round(25 + 8 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 2), 1)
            })
        
        df = pd.DataFrame(data)
        print(f"✅ Dados de exemplo gerados: {len(df)} amostras")
        return df
    
    def add_time_features(self, df):
        """Adiciona features temporais úteis"""
        print("🕐 Adicionando features temporais...")
        
        # Converter timestamp para datetime se necessário
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Features temporais
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['month'] = df['timestamp'].dt.month
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
            
            # Períodos do dia
            df['period'] = pd.cut(df['hour'], 
                    bins=[0, 6, 12, 18, 24],
                    labels=['noite', 'manha', 'tarde', 'anoitecer'],  # Labels únicos
                    include_lowest=True)
            
            # Features cíclicas para hora
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
            
            # Features cíclicas para dia da semana
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        return df
    
    def add_derived_features(self, df):
        """Adiciona features derivadas dos dados dos sensores"""
        print("🧮 Calculando features derivadas...")
        
        # Índice de qualidade do solo
        df['soil_quality_index'] = (
            df['phosphorus'] * 0.4 + 
            df['potassium'] * 0.4 + 
            ((df['ph_level'] >= 6.0) & (df['ph_level'] <= 7.5)).astype(int) * 0.2
        )
        
        # Stress hídrico
        df['water_stress'] = np.where(df['humidity'] < 30, 2,
                                     np.where(df['humidity'] < 40, 1, 0))
        
        # Necessidade de irrigação baseada em regras
        df['irrigation_rule_based'] = (
            (df['humidity'] < 35) |
            (df['ph_level'] < 6.0) |
            (df['ph_level'] > 7.5) |
            (df['phosphorus'] == 0) |
            (df['potassium'] == 0)
        ).astype(int)
        
        # Features de média móvel (se houver dados suficientes)
        if len(df) > 10:
            df['humidity_ma_5'] = df['humidity'].rolling(window=5, min_periods=1).mean()
            df['ph_ma_5'] = df['ph_level'].rolling(window=5, min_periods=1).mean()
            df['humidity_trend'] = df['humidity'] - df['humidity_ma_5']
        
        # Interações entre features
        df['ph_humidity_interaction'] = df['ph_level'] * df['humidity']
        df['nutrient_interaction'] = df['phosphorus'] * df['potassium']
        
        return df
    
    def clean_data(self, df):
        """Limpa e valida os dados"""
        print("🧹 Limpando dados...")
        
        initial_count = len(df)
        
        # Remover valores impossíveis
        df = df[df['humidity'].between(0, 100)]
        df = df[df['ph_level'].between(0, 14)]
        
        # Tratar valores ausentes
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = self.imputer.fit_transform(df[numeric_columns])
        
        # Remover outliers extremos usando IQR
        for col in ['humidity', 'ph_level']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[df[col].between(lower_bound, upper_bound)]
        
        cleaned_count = len(df)
        removed_count = initial_count - cleaned_count
        
        print(f"✅ Limpeza concluída: {removed_count} registros removidos ({removed_count/initial_count*100:.1f}%)")
        
        return df
    
    def prepare_features(self, df, target_column='pump_status'):
        """Prepara features para machine learning"""
        print("🎯 Preparando features para ML...")
        
        # Definir features para usar
        feature_columns = [
            'humidity', 'ph_level', 'phosphorus', 'potassium',
            'hour', 'day_of_week', 'soil_quality_index', 'water_stress',
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
            'ph_humidity_interaction', 'nutrient_interaction'
        ]
        
        # Remover colunas que não existem
        available_features = [col for col in feature_columns if col in df.columns]
        
        X = df[available_features]
        y = df[target_column] if target_column in df.columns else None
        
        print(f"📊 Features selecionadas: {len(available_features)}")
        print(f"   {', '.join(available_features)}")
        
        return X, y, available_features
    
    def get_feature_statistics(self, df):
        """Retorna estatísticas das features"""
        print("📈 Calculando estatísticas das features...")
        
        stats = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            stats[col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'missing_pct': (df[col].isnull().sum() / len(df)) * 100
            }
        
        return stats
    
    def prepare_complete_dataset(self):
        """Pipeline completo de preparação de dados"""
        print("🔄 Executando pipeline completo de preparação...")
        
        # Carregar dados
        df = self.load_sensor_data()
        
        # Adicionar features
        df = self.add_time_features(df)
        df = self.add_derived_features(df)
        
        # Limpar dados
        df = self.clean_data(df)
        
        # Preparar features
        X, y, feature_names = self.prepare_features(df)
        
        # Estatísticas
        stats = self.get_feature_statistics(df)
        
        print("✅ Pipeline de preparação concluído!")
        print(f"📊 Dataset final: {len(df)} amostras, {len(feature_names)} features")
        
        return {
            'dataframe': df,
            'features': X,
            'target': y,
            'feature_names': feature_names,
            'statistics': stats
        }

# Exemplo de uso
if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    result = preprocessor.prepare_complete_dataset()
    
    print("\n📋 RESUMO DO DATASET")
    print("=" * 40)
    print(f"Total de amostras: {len(result['dataframe'])}")
    print(f"Número de features: {len(result['feature_names'])}")
    
    if result['target'] is not None:
        print(f"Distribuição do target:")
        print(result['target'].value_counts().to_dict())
    
    print("\n📊 ESTATÍSTICAS PRINCIPAIS")
    print("=" * 40)
    for feature, stats in result['statistics'].items():
        if feature in ['humidity', 'ph_level', 'soil_quality_index']:
            print(f"{feature}:")
            print(f"  Média: {stats['mean']:.2f}")
            print(f"  Desvio: {stats['std']:.2f}")
            print(f"  Range: {stats['min']:.2f} - {stats['max']:.2f}")