import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from data_preprocessing import DataPreprocessor

class ModelTrainer:
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.preprocessor = DataPreprocessor()
        self.feature_names = []
        
    def initialize_models(self):
        """Inicializa diferentes modelos para comparação"""
        self.models = {
            'RandomForest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),
            'GradientBoosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            ),
            'LogisticRegression': LogisticRegression(
                random_state=42,
                max_iter=1000,
                C=1.0
            ),
            'SVM': SVC(
                kernel='rbf',
                C=1.0,
                probability=True,
                random_state=42
            )
        }
        
        print(f"🤖 Modelos inicializados: {', '.join(self.models.keys())}")
    
    def train_and_evaluate_models(self, X, y):
        """Treina e avalia todos os modelos"""
        print("🎯 Treinando e avaliando modelos...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Escalar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        results = {}
        
        for name, model in self.models.items():
            print(f"\n🔄 Treinando {name}...")
            
            # Treinar modelo
            model.fit(X_train_scaled, y_train)
            
            # Predições
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Métricas
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            
            results[name] = {
                'Model': model,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
                'CV_Mean': cv_scores.mean(),
                'CV_Std': cv_scores.std(),
                'Predictions': y_pred,
                'Probabilities': y_pred_proba
            }
            
            print(f"  Acurácia: {accuracy:.3f}")
            print(f"  Precisão: {precision:.3f}")
            print(f"  Recall: {recall:.3f}")
            print(f"  F1-Score: {f1:.3f}")
            print(f"  CV Score: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        # Encontrar melhor modelo
        best_model_name = max(results.keys(), key=lambda x: results[x]['F1-Score'])
        self.best_model = results[best_model_name]['Model']
        
        print(f"\n🏆 Melhor modelo: {best_model_name}")
        print(f"   F1-Score: {results[best_model_name]['F1-Score']:.3f}")
        
        return results, X_test, y_test
    
    def optimize_hyperparameters(self, X, y, model_name='RandomForest'):
        """Otimiza hiperparâmetros do modelo selecionado"""
        print(f"⚙️ Otimizando hiperparâmetros para {model_name}...")
        
        # Definir grid de parâmetros
        param_grids = {
            'RandomForest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'GradientBoosting': {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0]
            },
            'LogisticRegression': {
                'C': [0.1, 1.0, 10.0],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear', 'lbfgs']
            }
        }
        
        if model_name not in param_grids:
            print(f"❌ Parâmetros não definidos para {model_name}")
            return None
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Escalar
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Grid search
        base_model = self.models[model_name]
        grid_search = GridSearchCV(
            base_model,
            param_grids[model_name],
            cv=5,
            scoring='f1_weighted',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train_scaled, y_train)
        
        print(f"✅ Melhores parâmetros: {grid_search.best_params_}")
        print(f"✅ Melhor score: {grid_search.best_score_:.3f}")
        
        # Atualizar modelo
        self.models[model_name] = grid_search.best_estimator_
        self.best_model = grid_search.best_estimator_
        
        return grid_search.best_estimator_
    
    def analyze_feature_importance(self, model, feature_names):
        """Analisa importância das features"""
        print("🔍 Analisando importância das features...")
        
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("📊 Top 10 features mais importantes:")
            for i, (_, row) in enumerate(importance_df.head(10).iterrows()):
                print(f"  {i+1:2d}. {row['feature']:<20}: {row['importance']:.4f}")
            
            return importance_df
        else:
            print("⚠️ Modelo não suporta análise de importância de features")
            return None
    
    def generate_performance_report(self, results, X_test, y_test):
        """Gera relatório completo de performance"""
        print("\n📋 RELATÓRIO DE PERFORMANCE")
        print("=" * 50)
        
        # Tabela comparativa
        comparison_df = pd.DataFrame({
            'Modelo': list(results.keys()),
            'Acurácia': [results[model]['Accuracy'] for model in results],
            'Precisão': [results[model]['Precision'] for model in results],
            'Recall': [results[model]['Recall'] for model in results],
            'F1-Score': [results[model]['F1-Score'] for model in results],
            'CV Score': [results[model]['CV_Mean'] for model in results]
        })
        
        print(comparison_df.round(3).to_string(index=False))
        
        # Matriz de confusão do melhor modelo
        best_model_name = comparison_df.loc[comparison_df['F1-Score'].idxmax(), 'Modelo']
        best_predictions = results[best_model_name]['Predictions']
        
        print(f"\n🎯 Matriz de Confusão - {best_model_name}")
        print("-" * 30)
        cm = confusion_matrix(y_test, best_predictions)
        print(f"Verdadeiro Negativo: {cm[0,0]}")
        print(f"Falso Positivo: {cm[0,1]}")
        print(f"Falso Negativo: {cm[1,0]}")
        print(f"Verdadeiro Positivo: {cm[1,1]}")
        
        # Interpretação dos resultados
        print(f"\n💡 INTERPRETAÇÃO DOS RESULTADOS")
        print("-" * 35)
        
        accuracy = results[best_model_name]['Accuracy']
        if accuracy > 0.9:
            print("✅ Excelente: Modelo muito preciso para predição de irrigação")
        elif accuracy > 0.8:
            print("👍 Bom: Modelo adequado para uso em produção")
        elif accuracy > 0.7:
            print("⚠️ Aceitável: Modelo funcional, mas pode ser melhorado")
        else:
            print("❌ Insuficiente: Modelo precisa ser retreinado")
        
        return comparison_df
    
    def save_best_model(self, filepath='best_farmtech_model.pkl'):
        """Salva o melhor modelo"""
        if self.best_model is not None:
            model_data = {
                'model': self.best_model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'training_date': datetime.now().isoformat(),
                'model_type': type(self.best_model).__name__
            }
            
            joblib.dump(model_data, filepath)
            print(f"💾 Melhor modelo salvo em: {filepath}")
        else:
            print("❌ Nenhum modelo foi treinado ainda!")
    
    def complete_training_pipeline(self):
        """Pipeline completo de treinamento"""
        print("🚀 Iniciando pipeline completo de treinamento...")
        
        # Preparar dados
        data_result = self.preprocessor.prepare_complete_dataset()
        X = data_result['features']
        y = data_result['target']
        self.feature_names = data_result['feature_names']
        
        if y is None:
            print("❌ Target não encontrado nos dados!")
            return None
        
        # Inicializar modelos
        self.initialize_models()
        
        # Treinar e avaliar
        results, X_test, y_test = self.train_and_evaluate_models(X, y)
        
        # Gerar relatório
        comparison_df = self.generate_performance_report(results, X_test, y_test)
        
        # Analisar importância das features
        best_model_name = comparison_df.loc[comparison_df['F1-Score'].idxmax(), 'Modelo']
        importance_df = self.analyze_feature_importance(self.best_model, self.feature_names)
        
        # Salvar modelo
        self.save_best_model()
        
        print("\n🎉 Pipeline de treinamento concluído com sucesso!")
        
        return {
            'results': results,
            'comparison': comparison_df,
            'feature_importance': importance_df,
            'best_model': self.best_model
        }

# Execução principal
if __name__ == "__main__":
    trainer = ModelTrainer()
    pipeline_result = trainer.complete_training_pipeline()
    
    if pipeline_result:
        print(f"\n🏆 Melhor modelo: {type(pipeline_result['best_model']).__name__}")
        print("✅ Modelo pronto para uso em produção!")