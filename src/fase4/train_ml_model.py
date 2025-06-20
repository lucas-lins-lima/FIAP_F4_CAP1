import sys
import os
sys.path.append('scr/fase4/machine_learning')

from irrigation_predictor import IrrigationPredictor

def train_model():
    print("🤖 Treinando modelo de Machine Learning...")
    
    predictor = IrrigationPredictor()
    accuracy = predictor.train_model()
    
    if accuracy:
        predictor.save_model('farmtech_irrigation_model.pkl')
        print(f"✅ Modelo treinado com sucesso! Acurácia: {accuracy:.2%}")
    else:
        print("❌ Erro no treinamento do modelo")

if __name__ == "__main__":
    train_model()