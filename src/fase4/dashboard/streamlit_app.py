import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Configurar página
st.set_page_config(
    page_title="FarmTech Solutions - Dashboard v4.0",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adicionar caminhos para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../machine_learning'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../integration'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../fase3/python'))

class FarmTechDashboard:
    def __init__(self):
        self.db = None
        self.predictor = None
        self.init_database()
        self.init_ml_model()
        
    def init_database(self):
        """Inicializa conexão com banco de dados"""
        try:
            from database_enhanced import EnhancedFarmTechDatabase
            self.db = EnhancedFarmTechDatabase()
        except ImportError:
            try:
                from database_manager import FarmTechDatabase
                self.db = FarmTechDatabase()
            except ImportError:
                st.warning("⚠️ Usando dados mock (banco de dados não disponível)")
                self.db = None
    
    def init_ml_model(self):
        """Inicializa modelo de ML (opcional)"""
        try:
            from irrigation_predictor import IrrigationPredictor
            self.predictor = IrrigationPredictor()
            
            # Tentar carregar modelo existente
            model_path = 'farmtech_irrigation_model.pkl'
            if os.path.exists(model_path):
                self.predictor.load_model(model_path)
            else:
                # Treinar modelo básico se não existir
                with st.spinner("🤖 Treinando modelo de ML pela primeira vez..."):
                    self.predictor.train_model()
                    self.predictor.save_model(model_path)
                st.success("✅ Modelo ML treinado com sucesso!")
                
        except Exception as e:
            st.info(f"ℹ️ ML não disponível: Usando sistema básico")
            self.predictor = None
    
    def safe_convert_data(self, df):
        """Converte dados para tipos seguros para JSON"""
        if df.empty:
            return df
        
        # Fazer cópia para não modificar original
        safe_df = df.copy()
        
        # Converter timestamp para string se necessário
        if 'timestamp' in safe_df.columns:
            safe_df['timestamp'] = pd.to_datetime(safe_df['timestamp'], errors='coerce')
            safe_df = safe_df.dropna(subset=['timestamp'])
        
        # Converter colunas numéricas para float básico
        numeric_columns = ['humidity', 'ph_level']
        for col in numeric_columns:
            if col in safe_df.columns:
                safe_df[col] = pd.to_numeric(safe_df[col], errors='coerce')
                safe_df[col] = safe_df[col].fillna(0).astype(float)
        
        # Converter colunas boolean para int
        bool_columns = ['phosphorus', 'potassium', 'pump_status']
        for col in bool_columns:
            if col in safe_df.columns:
                safe_df[col] = safe_df[col].astype(bool).astype(int)
        
        # Remover linhas com valores inválidos
        safe_df = safe_df.replace([np.inf, -np.inf], np.nan).dropna()
        
        return safe_df
    
    def load_data(self):
        """Carrega dados do banco de dados"""
        if not self.db:
            return self.create_mock_data()
            
        try:
            if hasattr(self.db, 'get_sensor_data'):
                data = self.db.get_sensor_data(limit=500)
            else:
                data = []
                
            if not data:
                # Gerar dados de exemplo se não houver dados
                self.generate_sample_data()
                if hasattr(self.db, 'get_sensor_data'):
                    data = self.db.get_sensor_data(limit=500)
            
            if data:
                df = pd.DataFrame(data)
                return self.safe_convert_data(df)
            else:
                return self.create_mock_data()
                
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar dados do banco: {str(e)}")
            return self.create_mock_data()
    
    def create_mock_data(self):
        """Cria dados mock seguros para demonstração"""
        np.random.seed(42)
        
        # Criar 100 pontos de dados nas últimas 48 horas
        num_points = 100
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=48)
        
        # Criar timestamps
        timestamps = pd.date_range(start=start_time, end=end_time, periods=num_points)
        
        # Gerar dados realistas
        data = []
        for i, timestamp in enumerate(timestamps):
            hour = timestamp.hour
            
            # Padrão de umidade baseado na hora (mais baixa durante o dia)
            base_humidity = 45 + 10 * np.sin(2 * np.pi * (hour - 6) / 24)
            humidity = float(np.clip(base_humidity + np.random.normal(0, 8), 10, 90))
            
            # pH com variação pequena
            ph_level = float(np.clip(6.8 + np.random.normal(0, 0.6), 4.5, 8.5))
            
            # Nutrientes com probabilidade
            phosphorus = int(np.random.random() > 0.3)
            potassium = int(np.random.random() > 0.25)
            
            # Lógica de irrigação
            pump_status = int((humidity < 35) or (ph_level < 6.0) or (ph_level > 7.5) or (phosphorus == 0) or (potassium == 0))
            
            data.append({
                'id': i + 1,
                'timestamp': timestamp,
                'humidity': humidity,
                'ph_level': ph_level,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'pump_status': pump_status
            })
        
        df = pd.DataFrame(data)
        return self.safe_convert_data(df)
    
    def generate_sample_data(self, n_samples=50):
        """Gera dados de exemplo para o banco"""
        if not self.db:
            return
            
        try:
            base_time = datetime.now() - timedelta(hours=24)
            
            for i in range(n_samples):
                timestamp = base_time + timedelta(minutes=i*30)
                hour = timestamp.hour
                
                # Simular padrões realistas
                humidity = max(15, min(85, 40 + 15 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 8)))
                ph = max(4.5, min(8.5, np.random.normal(6.7, 0.6)))
                phosphorus = np.random.choice([True, False], p=[0.7, 0.3])
                potassium = np.random.choice([True, False], p=[0.75, 0.25])
                
                pump_active = (humidity < 35) or (ph < 6.0 or ph > 7.5) or (not phosphorus or not potassium)
                
                if hasattr(self.db, 'insert_enhanced_sensor_data'):
                    self.db.insert_enhanced_sensor_data(humidity, ph, phosphorus, potassium, pump_active)
                elif hasattr(self.db, 'insert_sensor_data'):
                    self.db.insert_sensor_data(humidity, ph, phosphorus, potassium, pump_active)
                    
        except Exception as e:
            st.warning(f"⚠️ Erro ao gerar dados: {e}")
    
    def create_realtime_metrics(self, df):
        """Cria métricas em tempo real"""
        if df.empty:
            st.error("📭 Nenhum dado disponível")
            return
        
        latest = df.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            delta_humidity = None
            if len(df) > 1:
                delta_humidity = float(latest['humidity'] - df.iloc[-2]['humidity'])
            
            st.metric(
                label="💧 Umidade do Solo",
                value=f"{latest['humidity']:.1f}%",
                delta=f"{delta_humidity:.1f}%" if delta_humidity is not None else None
            )
        
        with col2:
            delta_ph = None
            if len(df) > 1:
                delta_ph = float(latest['ph_level'] - df.iloc[-2]['ph_level'])
            
            st.metric(
                label="🧪 Nível de pH",
                value=f"{latest['ph_level']:.2f}",
                delta=f"{delta_ph:.2f}" if delta_ph is not None else None
            )
        
        with col3:
            nutrient_status = "✅ OK" if latest['phosphorus'] and latest['potassium'] else "⚠️ Baixo"
            st.metric(
                label="🌱 Nutrientes",
                value=nutrient_status
            )
        
        with col4:
            pump_status = "🔴 ATIVA" if latest['pump_status'] else "⚫ INATIVA"
            st.metric(
                label="💦 Bomba de Irrigação",
                value=pump_status
            )
    
    def create_safe_charts(self, df):
        """Cria gráficos seguros usando plotly express"""
        if df.empty:
            st.warning("📭 Sem dados para gráficos")
            return
            
        try:
            # Preparar dados seguros
            chart_data = df.copy()
            
            # Converter timestamp para string para evitar problemas de serialização
            chart_data['time_str'] = chart_data['timestamp'].dt.strftime('%H:%M')
            chart_data['date_str'] = chart_data['timestamp'].dt.strftime('%m-%d %H:%M')
            
            # Limitar dados para performance
            if len(chart_data) > 50:
                chart_data = chart_data.tail(50)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💧 Umidade do Solo")
                fig_humidity = px.line(
                    chart_data, 
                    x='date_str', 
                    y='humidity',
                    title="Variação da Umidade (%)",
                    labels={'humidity': 'Umidade (%)', 'date_str': 'Data/Hora'}
                )
                fig_humidity.add_hline(y=30, line_dash="dash", line_color="red", 
                                     annotation_text="Crítico")
                fig_humidity.add_hline(y=70, line_dash="dash", line_color="green", 
                                     annotation_text="Ideal")
                fig_humidity.update_xaxes(tickangle=45)
                st.plotly_chart(fig_humidity, use_container_width=True)
            
            with col2:
                st.subheader("🧪 Nível de pH")
                fig_ph = px.line(
                    chart_data, 
                    x='date_str', 
                    y='ph_level',
                    title="Variação do pH",
                    labels={'ph_level': 'pH', 'date_str': 'Data/Hora'}
                )
                fig_ph.add_hrect(y0=6.0, y1=7.5, fillcolor="green", opacity=0.2,
                               annotation_text="Faixa Ideal")
                fig_ph.update_xaxes(tickangle=45)
                st.plotly_chart(fig_ph, use_container_width=True)
            
            # Gráfico de barras para nutrientes
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("🌱 Status dos Nutrientes")
                
                # Calcular percentuais
                phosphorus_pct = (chart_data['phosphorus'].sum() / len(chart_data)) * 100
                potassium_pct = (chart_data['potassium'].sum() / len(chart_data)) * 100
                
                nutrient_data = pd.DataFrame({
                    'Nutriente': ['Fósforo (P)', 'Potássio (K)'],
                    'Disponibilidade (%)': [phosphorus_pct, potassium_pct]
                })
                
                fig_nutrients = px.bar(
                    nutrient_data, 
                    x='Nutriente', 
                    y='Disponibilidade (%)',
                    title="Disponibilidade de Nutrientes",
                    color='Disponibilidade (%)',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig_nutrients, use_container_width=True)
            
            with col4:
                st.subheader("💦 Atividade da Bomba")
                
                # Status da bomba nas últimas leituras
                pump_activity = chart_data['pump_status'].value_counts()
                pump_labels = ['Inativa', 'Ativa']
                pump_values = [pump_activity.get(0, 0), pump_activity.get(1, 0)]
                
                fig_pump = px.pie(
                    values=pump_values,
                    names=pump_labels,
                    title="Status da Bomba",
                    color_discrete_map={'Ativa': '#ff4444', 'Inativa': '#44ff44'}
                )
                st.plotly_chart(fig_pump, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Erro ao criar gráficos: {e}")
            st.info("💡 Usando visualização alternativa...")
            
            # Fallback: mostrar dados em tabela
            st.subheader("📊 Dados Recentes")
            display_df = df.tail(10).copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%H:%M:%S')
            st.dataframe(display_df)
    
    def create_ml_predictions_section(self, df):
        """Seção de predições com Machine Learning"""
        if not self.predictor:
            st.info("🤖 Machine Learning não disponível. Execute: `py train_ml_model.py`")
            return
        
        if df.empty:
            st.warning("📭 Sem dados para predição")
            return
        
        st.header("🤖 Predições com Machine Learning")
        
        try:
            latest = df.iloc[-1]
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("🔮 Predição Atual")
                
                prediction = self.predictor.predict_irrigation(
                    humidity=float(latest['humidity']),
                    ph_level=float(latest['ph_level']),
                    phosphorus=bool(latest['phosphorus']),
                    potassium=bool(latest['potassium'])
                )
                
                if prediction['irrigation_needed']:
                    st.error(f"🚨 IRRIGAÇÃO RECOMENDADA")
                    st.write(f"**Confiança:** {prediction['confidence']:.1%}")
                else:
                    st.success(f"✅ IRRIGAÇÃO NÃO NECESSÁRIA")
                    st.write(f"**Confiança:** {prediction['confidence']:.1%}")
                
                # Mostrar probabilidades
                st.write("**Probabilidades:**")
                st.write(f"- Não irrigar: {prediction['probability_no']:.1%}")
                st.write(f"- Irrigar: {prediction['probability_yes']:.1%}")
            
            with col2:
                st.subheader("⏰ Predições Futuras")
                
                future_predictions = self.predictor.predict_next_hours(
                    current_humidity=float(latest['humidity']),
                    current_ph=float(latest['ph_level']),
                    current_phosphorus=bool(latest['phosphorus']),
                    current_potassium=bool(latest['potassium']),
                    hours_ahead=6
                )
                
                for pred in future_predictions:
                    hour = (datetime.now().hour + pred['hour_offset']) % 24
                    status = "🔴 IRRIGAR" if pred['irrigation_needed'] else "🟢 OK"
                    st.write(f"**Em {pred['hour_offset']}h ({hour:02d}:00)**: {status} "
                            f"(Conf: {pred['confidence']:.1%})")
                    
        except Exception as e:
            st.error(f"❌ Erro nas predições de ML: {e}")
    
    def create_system_alerts(self, df):
        """Sistema de alertas"""
        if df.empty:
            return
        
        latest = df.iloc[-1]
        alerts = []
        
        # Verificar condições críticas
        if latest['humidity'] < 25:
            alerts.append("🚨 CRÍTICO: Umidade extremamente baixa!")
        elif latest['humidity'] < 35:
            alerts.append("⚠️ ATENÇÃO: Umidade abaixo do ideal")
        
        if latest['ph_level'] < 5.5 or latest['ph_level'] > 8.0:
            alerts.append("🧪 ALERTA: pH fora da faixa recomendada")
        
        if not latest['phosphorus']:
            alerts.append("🟡 NUTRIENTE: Fósforo insuficiente")
        
        if not latest['potassium']:
            alerts.append("🔵 NUTRIENTE: Potássio insuficiente")
        
        if alerts:
            st.error("🚨 **ALERTAS DO SISTEMA**")
            for alert in alerts:
                st.write(f"- {alert}")
        else:
            st.success("✅ **Sistema funcionando normalmente**")
    
    def main(self):
        """Função principal do dashboard"""
        # Header
        st.title("🌾 FarmTech Solutions - Dashboard v4.0")
        st.markdown("**Sistema Inteligente de Agricultura Digital**")
        
        # Sidebar
        st.sidebar.header("⚙️ Configurações")
        st.sidebar.markdown("### 📊 Controles do Dashboard")
        
        # Controles da sidebar
        show_raw_data = st.sidebar.checkbox("📋 Mostrar Dados Brutos", value=False)
        auto_refresh = st.sidebar.checkbox("🔄 Atualização Automática", value=False)
        
        if auto_refresh:
            st.sidebar.info("🔄 Página será atualizada automaticamente")
            
        # Botão de atualização manual
        if st.sidebar.button("🔄 Atualizar Dados"):
            st.rerun()
        
        # Carregar dados
        with st.spinner("📊 Carregando dados..."):
            df = self.load_data()
        
        if df.empty:
            st.error("❌ Nenhum dado encontrado!")
            st.info("💡 Verifique se o banco de dados está configurado corretamente.")
            return
        
        # Mostrar informações básicas
        st.sidebar.markdown("### 📊 Informações dos Dados")
        st.sidebar.write(f"**Total de registros:** {len(df)}")
        st.sidebar.write(f"**Período:** {df['timestamp'].min().strftime('%d/%m %H:%M')} - {df['timestamp'].max().strftime('%d/%m %H:%M')}")
        
        # Métricas em tempo real
        st.header("📊 Métricas em Tempo Real")
        self.create_realtime_metrics(df)
        
        # Alertas do sistema
        st.header("🚨 Status do Sistema")
        self.create_system_alerts(df)
        
        # Gráficos principais
        st.header("📈 Análise Temporal")
        self.create_safe_charts(df)
        
        # Machine Learning
        if self.predictor:
            self.create_ml_predictions_section(df)
        
        # Dados brutos
        if show_raw_data:
            st.header("📋 Dados Brutos")
            display_df = df.copy()
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
            st.dataframe(display_df)
        
        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**FarmTech Solutions v4.0**")
        with col2:
            st.markdown("Desenvolvido para FIAP")
        with col3:
            st.markdown("Sistema de Agricultura Digital")
        
        # Auto refresh
        if auto_refresh:
            import time
            time.sleep(10)
            st.rerun()

# Executar aplicação
if __name__ == "__main__":
    dashboard = FarmTechDashboard()
    dashboard.main()