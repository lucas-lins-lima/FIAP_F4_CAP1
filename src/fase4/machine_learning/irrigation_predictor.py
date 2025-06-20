import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class IrrigationPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['humidity', 'ph_level', 'phosphorus', 'potassium', 'hour', 'temp_avg']
        self.model_trained = False
        
    def generate_training_data(self, n_samples=2000):
        """Gera dados sintéticos para treinamento baseados em padrões reais"""
        print("🔄 Gerando dados de treinamento...")
        
        np.random.seed(42)
        data = []
        
        for _ in range(n_samples):
            # Simular padrões realistas
            hour = np.random.randint(0, 24)
            
            # Umidade varia por horário (menor durante o dia)
            base_humidity = 45 + 10 * np.sin(2 * np.pi * hour / 24)
            humidity = max(10, min(90, np.random.normal(base_humidity, 12)))
            
            # pH varia ligeiramente
            ph_level = np.random.normal(6.8, 0.8)
            ph_level = max(4.0, min(9.0, ph_level))
            
            # Temperatura média simulada
            temp_avg = 25 + 8 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 2)
            temp_avg = max(15, min(40, temp_avg))
            
            # Nutrientes com correlação
            soil_quality = np.random.random()
            phosphorus = 1 if soil_quality > 0.3 else 0
            potassium = 1 if soil_quality > 0.25 else 0
            
            # Lógica de irrigação baseada em múltiplos fatores
            irrigation_needed = (
                (humidity < 35) or
                (ph_level < 6.0 or ph_level > 7.5) or
                (phosphorus == 0 or potassium == 0) or
                (temp_avg > 32 and humidity < 45) or
                (hour >= 6 and hour <= 18 and humidity < 40)  # Irrigar durante o dia se necessário
            )
            
            # Adicionar algum ruído para tornar mais realista
            if np.random.random() < 0.1:
                irrigation_needed = not irrigation_needed
            
            data.append([
                humidity, ph_level, phosphorus, potassium, 
                hour, temp_avg, int(irrigation_needed)
            ])
        
        columns = self.feature_names + ['irrigation_needed']
        df = pd.DataFrame(data, columns=columns)
        
        print(f"✅ Dados gerados: {len(df)} amostras")
        print(f"📊 Distribuição da irrigação: {df['irrigation_needed'].value_counts().to_dict()}")
        
        return df
    
    def train_model(self, df=None):
        """Treina o modelo de predição"""
        if df is None:
            df = self.generate_training_data()
        
        print("🧠 Treinando modelo de Machine Learning...")
        
        # Preparar dados
        X = df[self.feature_names]
        y = df['irrigation_needed']
        
        # Dividir em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar dados
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar múltiplos modelos
        models = {
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
            'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        best_model = None
        best_score = 0
        
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            score = accuracy_score(y_test, y_pred)
            
            print(f"📈 {name}: Acurácia = {score:.3f}")
            
            if score > best_score:
                best_score = score
                best_model = model
                self.model = model
        
        # Avaliar melhor modelo
        y_pred_best = self.model.predict(X_test_scaled)
        
        print(f"\n🏆 Melhor modelo: {type(self.model).__name__}")
        print(f"🎯 Acurácia final: {best_score:.3f}")
        print("\n📊 Relatório de classificação:")
        print(classification_report(y_test, y_pred_best))
        
        # Importância das features (se RandomForest)
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\n🔍 Importância das características:")
            for _, row in feature_importance.iterrows():
                print(f"  {row['feature']}: {row['importance']:.3f}")
        
        self.model_trained = True
        return best_score
    
    def predict_irrigation(self, humidity, ph_level, phosphorus, potassium, hour=None, temp_avg=25):
        """Prediz se irrigação é necessária"""
        if not self.model_trained:
            print("⚠️ Modelo não treinado! Treinando agora...")
            self.train_model()
        
        if hour is None:
            hour = datetime.now().hour
        
        # Preparar dados
        features = np.array([[humidity, ph_level, phosphorus, potassium, hour, temp_avg]])
        features_scaled = self.scaler.transform(features)
        
        # Predição
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return {
            'irrigation_needed': bool(prediction),
            'probability_no': probability[0],
            'probability_yes': probability[1],
            'confidence': max(probability)
        }
    
    def predict_next_hours(self, current_humidity, current_ph, current_phosphorus, 
                          current_potassium, hours_ahead=6):
        """Prediz necessidade de irrigação para as próximas horas"""
        predictions = []
        
        for hour_offset in range(1, hours_ahead + 1):
            future_hour = (datetime.now().hour + hour_offset) % 24
            
            # Simular mudanças graduais na umidade
            humidity_decay = current_humidity - (hour_offset * 2)  # Umidade diminui ~2% por hora
            humidity_decay = max(10, humidity_decay)
            
            pred = self.predict_irrigation(
                humidity=humidity_decay,
                ph_level=current_ph,
                phosphorus=current_phosphorus,
                potassium=current_potassium,
                hour=future_hour
            )
            
            predictions.append({
                'hour_offset': hour_offset,
                'future_hour': future_hour,
                'predicted_humidity': humidity_decay,
                'irrigation_needed': pred['irrigation_needed'],
                'confidence': pred['confidence']
            })
        
        return predictions
    
    def save_model(self, filepath='farmtech_irrigation_model.pkl'):
        """Salva o modelo treinado"""
        if self.model_trained:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'trained_at': datetime.now().isoformat()
            }
            joblib.dump(model_data, filepath)
            print(f"💾 Modelo salvo em: {filepath}")
        else:
            print("⚠️ Modelo não treinado ainda!")
    
    def load_model(self, filepath='farmtech_irrigation_model.pkl'):
        """Carrega modelo salvo"""
        try:
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_names = model_data['feature_names']
            self.model_trained = True
            print(f"✅ Modelo carregado de: {filepath}")
            print(f"📅 Treinado em: {model_data.get('trained_at', 'Data desconhecida')}")
        except FileNotFoundError:
            print(f"❌ Arquivo {filepath} não encontrado!")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")

# Exemplo de uso e teste
if __name__ == "__main__":
    # Criar e treinar o preditor
    predictor = IrrigationPredictor()
    
    # Treinar modelo
    accuracy = predictor.train_model()
    
    # Salvar modelo
    predictor.save_model()
    
    # Testar predições
    print("\n🔮 TESTE DE PREDIÇÕES")
    print("=" * 40)
    
    test_cases = [
        {"humidity": 25, "ph_level": 6.5, "phosphorus": 1, "potassium": 1, "description": "Umidade baixa"},
        {"humidity": 55, "ph_level": 7.0, "phosphorus": 1, "potassium": 1, "description": "Condições ideais"},
        {"humidity": 40, "ph_level": 5.5, "phosphorus": 0, "potassium": 0, "description": "pH baixo, sem nutrientes"},
        {"humidity": 45, "ph_level": 8.0, "phosphorus": 1, "potassium": 1, "description": "pH alto"},
    ]
    
    for case in test_cases:
        desc = case.pop('description')
        result = predictor.predict_irrigation(**case)
        
        print(f"\n📝 Caso: {desc}")
        print(f"   Dados: {case}")
        print(f"   Irrigar: {'✅ SIM' if result['irrigation_needed'] else '❌ NÃO'}")
        print(f"   Confiança: {result['confidence']:.2%}")
    
    # Teste de predição para próximas horas
    print("\n🕐 PREDIÇÃO PARA PRÓXIMAS HORAS")
    print("=" * 40)
    
    future_predictions = predictor.predict_next_hours(
        current_humidity=35,
        current_ph=6.8,
        current_phosphorus=1,
        current_potassium=1,
        hours_ahead=6
    )
    
    for pred in future_predictions:
        status = "✅ IRRIGAR" if pred['irrigation_needed'] else "⏸️ AGUARDAR"
        print(f"Em {pred['hour_offset']}h (às {pred['future_hour']:02d}:00): {status} "
              f"(Umidade: {pred['predicted_humidity']:.1f}%, Confiança: {pred['confidence']:.1%})")