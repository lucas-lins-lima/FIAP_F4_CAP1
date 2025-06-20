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
import joblib

# Configurar página
st.set_page_config(
    page_title="FarmTech Solutions - Dashboard v4.0",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Adicionar caminhos para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../machine_learning'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../fase3/python'))

try:
    from irrigation_predictor import IrrigationPredictor
    from database_manager import FarmTechDatabase
except ImportError:
    st.error("⚠️ Módulos não encontrados. Certifique-se de que todos os arquivos estão no lugar correto.")
    st.stop()

class FarmTechDashboard:
    def __init__(self):
        self.db = FarmTechDatabase()
        self.predictor = IrrigationPredictor()
        
        # Tentar carregar modelo treinado
        try:
            self.predictor.load_model('farmtech_irrigation_model.pkl')
        except:
            st.warning("⚠️ Modelo ML não encontrado. Treinando novo modelo...")
            self.predictor.train_model()
            self.predictor.save_model()
    
    def load_data(self):
        """Carrega dados do banco de dados"""
        data = self.db.get_sensor_data(limit=500)
        if not data:
            # Gerar dados de exemplo se não houver dados
            self.generate_sample_data()
            data = self.db.get_sensor_data(limit=500)
        
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def generate_sample_data(self, n_samples=200):
        """Gera dados de exemplo para demonstração"""
        np.random.seed(42)
        base_time = datetime.now() - timedelta(hours=48)
        
        for i in range(n_samples):
            timestamp = base_time + timedelta(minutes=i*15)
            hour = timestamp.hour
            
            # Simular padrões realistas
            humidity = max(15, min(85, 40 + 15 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 8)))
            ph = max(4.5, min(8.5, np.random.normal(6.7, 0.6)))
            phosphorus = np.random.choice([True, False], p=[0.7, 0.3])
            potassium = np.random.choice([True, False], p=[0.75, 0.25])
            
            # Lógica de irrigação
            pump_active = (humidity < 35) or (ph < 6.0 or ph > 7.5) or (not phosphorus or not potassium)
            
            self.db.insert_sensor_data(humidity, ph, phosphorus, potassium, pump_active)
    
    def create_realtime_metrics(self, df):
        """Cria métricas em tempo real"""
        if df.empty:
            return
        
        latest = df.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            delta_humidity = df['humidity'].iloc[-1] - df['humidity'].iloc[-2] if len(df) > 1 else 0
            st.metric(
                label="💧 Umidade do Solo",
                value=f"{latest['humidity']:.1f}%",
                delta=f"{delta_humidity:.1f}%"
            )
        
        with col2:
            delta_ph = df['ph_level'].iloc[-1] - df['ph_level'].iloc[-2] if len(df) > 1 else 0
            st.metric(
                label="🧪 Nível de pH",
                value=f"{latest['ph_level']:.2f}",
                delta=f"{delta_ph:.2f}"
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
    
    def create_time_series_chart(self, df):
        """Cria gráfico de séries temporais"""
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Umidade do Solo (%)', 'Nível de pH', 'Status da Bomba'),
            vertical_spacing=0.08,
            shared_xaxes=True
        )
        
        # Umidade
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['humidity'],
                mode='lines+markers',
                name='Umidade',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4)
            ),
            row=1, col=1
        )
        
        # Linha de referência para umidade crítica
        fig.add_hline(y=30, line_dash="dash", line_color="red", 
                     annotation_text="Crítico", row=1, col=1)
        
        # pH
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['ph_level'],
                mode='lines+markers',
                name='pH',
                line=dict(color='#ff7f0e', width=2),
                marker=dict(size=4)
            ),
            row=2, col=1
        )
        
        # Faixa ideal de pH
        fig.add_hrect(y0=6.0, y1=7.5, fillcolor="green", opacity=0.2,
                     annotation_text="Faixa Ideal", row=2, col=1)
        
        # Status da bomba
        fig.add_trace(
            go.Scatter(
                x=df['timestamp'],
                y=df['pump_status'],
                mode='lines+markers',
                name='Bomba',
                line=dict(color='#d62728', width=3),
                marker=dict(size=6)
            ),
            row=3, col=1
        )
        
        fig.update_layout(
            height=600,
            title_text="📊 Monitoramento em Tempo Real - Últimas 48h",
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Horário", row=3, col=1)
        
        return fig
    
    def create_correlation_heatmap(self, df):
        """Cria mapa de calor de correlações"""
        corr_data = df[['humidity', 'ph_level', 'phosphorus', 'potassium', 'pump_status']].corr()
        
        fig = px.imshow(
            corr_data,
            title="🔥 Matriz de Correlação dos Sensores",
            color_continuous_scale="RdBu_r",
            aspect="auto",
            text_auto=True
        )
        
        fig.update_layout(height=400)
        return fig
    
    def create_nutrient_analysis(self, df):
        """Análise de nutrientes"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza para fósforo
            phosphorus_counts = df['phosphorus'].value_counts()
            fig_p = px.pie(
                values=phosphorus_counts.values,
                names=['Presente' if x else 'Ausente' for x in phosphorus_counts.index],
                title="🟡 Disponibilidade de Fósforo (P)",
                color_discrete_map={'Presente': '#2ecc71', 'Ausente': '#e74c3c'}
            )
            st.plotly_chart(fig_p, use_container_width=True)
        
        with col2:
            # Gráfico de pizza para potássio
            potassium_counts = df['potassium'].value_counts()
            fig_k = px.pie(
                values=potassium_counts.values,
                names=['Presente' if x else 'Ausente' for x in potassium_counts.index],
                title="🔵 Disponibilidade de Potássio (K)",
                color_discrete_map={'Presente': '#3498db', 'Ausente': '#e67e22'}
            )
            st.plotly_chart(fig_k, use_container_width=True)
    
    def create_irrigation_efficiency_chart(self, df):
        """Análise de eficiência da irrigação"""
        # Calcular eficiência por hora
        df['hour'] = df['timestamp'].dt.hour
        hourly_stats = df.groupby('hour').agg({
            'pump_status': ['sum', 'count'],
            'humidity': 'mean'
        }).round(2)
        
        hourly_stats.columns = ['irrigation_count', 'total_readings', 'avg_humidity']
        hourly_stats['irrigation_rate'] = (hourly_stats['irrigation_count'] / hourly_stats['total_readings'] * 100).round(1)
        hourly_stats = hourly_stats.reset_index()
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Taxa de Irrigação por Hora (%)', 'Umidade Média por Hora'),
            vertical_spacing=0.15
        )
        
        # Taxa de irrigação
        fig.add_trace(
            go.Bar(
                x=hourly_stats['hour'],
                y=hourly_stats['irrigation_rate'],
                name='Taxa de Irrigação',
                marker_color='lightblue'
            ),
            row=1, col=1
        )
        
        # Umidade média
        fig.add_trace(
            go.Scatter(
                x=hourly_stats['hour'],
                y=hourly_stats['avg_humidity'],
                mode='lines+markers',
                name='Umidade Média',
                line=dict(color='green', width=3)
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=500,
            title_text="⚡ Análise de Eficiência da Irrigação",
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Hora do Dia", row=2, col=1)
        
        return fig
    
    def create_ml_predictions_section(self, df):
        """Seção de predições com Machine Learning"""
        st.header("🤖 Predições com Machine Learning")
        
        if df.empty:
            st.warning("Sem dados para predição")
            return
        
        latest = df.iloc[-1]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔮 Predição Atual")
            
            # Predição atual
            prediction = self.predictor.predict_irrigation(
                humidity=latest['humidity'],
                ph_level=latest['ph_level'],
                phosphorus=latest['phosphorus'],
                potassium=latest['potassium']
            )
            
            if prediction['irrigation_needed']:
                st.error(f"🚨 IRRIGAÇÃO RECOMENDADA (Confiança: {prediction['confidence']:.1%})")
            else:
                st.success(f"✅ IRRIGAÇÃO NÃO NECESSÁRIA (Confiança: {prediction['confidence']:.1%})")
            
            # Mostrar probabilidades
            st.write("**Probabilidades:**")
            st.write(f"- Não irrigar: {prediction['probability_no']:.1%}")
            st.write(f"- Irrigar: {prediction['probability_yes']:.1%}")
        
        with col2:
            st.subheader("⏰ Predições Futuras")
            
            # Predições para próximas horas
            future_predictions = self.predictor.predict_next_hours(
                current_humidity=latest['humidity'],
                current_ph=latest['ph_level'],
                current_phosphorus=latest['phosphorus'],
                current_potassium=latest['potassium'],
                hours_ahead=6
            )
            
            for pred in future_predictions:
                hour = (datetime.now().hour + pred['hour_offset']) % 24
                status = "🔴 IRRIGAR" if pred['irrigation_needed'] else "🟢 OK"
                st.write(f"**{pred['hour_offset']}h ({hour:02d}:00)**: {status} "
                        f"(Conf: {pred['confidence']:.1%})")
    
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
        
        # Verificar tendências
        if len(df) >= 5:
            recent_humidity = df['humidity'].tail(5)
            if recent_humidity.is_monotonic_decreasing:
                alerts.append("📉 TENDÊNCIA: Umidade em queda constante")
        
        if alerts:
            st.error("🚨 **ALERTAS DO SISTEMA**")
            for alert in alerts:
                st.write(f"- {alert}")
        else:
            st.success("✅ **Sistema funcionando normalmente**")
    
    def create_data_export_section(self, df):
        """Seção para exportar dados"""
        st.subheader("💾 Exportar Dados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exportar CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"farmtech_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📈 Relatório Estatístico"):
                stats = df.describe()
                st.dataframe(stats)
        
        with col3:
            if st.button("🔄 Atualizar Dados"):
                st.rerun()
    
    def main(self):
        """Função principal do dashboard"""
        # Header
        st.title("🌾 FarmTech Solutions - Dashboard v4.0")
        st.markdown("**Sistema Inteligente de Agricultura Digital**")
        
        # Sidebar
        st.sidebar.header("⚙️ Configurações")
        st.sidebar.markdown("### 📊 Controles do Dashboard")
        
        # Controles da sidebar
        auto_refresh = st.sidebar.checkbox("🔄 Atualização Automática", value=False)
        show_raw_data = st.sidebar.checkbox("📋 Mostrar Dados Brutos", value=False)
        
        # Período de dados
        data_period = st.sidebar.selectbox(
            "📅 Período dos Dados",
            ["Últimas 6 horas", "Últimas 24 horas", "Últimos 3 dias", "Todos os dados"]
        )
        
        # Carregar dados
        df = self.load_data()
        
        # Filtrar por período
        now = datetime.now()
        if data_period == "Últimas 6 horas":
            df = df[df['timestamp'] >= now - timedelta(hours=6)]
        elif data_period == "Últimas 24 horas":
            df = df[df['timestamp'] >= now - timedelta(hours=24)]
        elif data_period == "Últimos 3 dias":
            df = df[df['timestamp'] >= now - timedelta(days=3)]
        
        if df.empty:
            st.error("❌ Nenhum dado encontrado para o período selecionado!")
            return
        
        # Métricas em tempo real
        st.header("📊 Métricas em Tempo Real")
        self.create_realtime_metrics(df)
        
        # Alertas do sistema
        st.header("🚨 Status do Sistema")
        self.create_system_alerts(df)
        
        # Gráficos principais
        st.header("📈 Análise Temporal")
        fig_time = self.create_time_series_chart(df)
        st.plotly_chart(fig_time, use_container_width=True)
        
        # Análise de correlação
        col1, col2 = st.columns(2)
        
        with col1:
            fig_corr = self.create_correlation_heatmap(df)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with col2:
            fig_efficiency = self.create_irrigation_efficiency_chart(df)
            st.plotly_chart(fig_efficiency, use_container_width=True)
        
        # Análise de nutrientes
        st.header("🌱 Análise de Nutrientes")
        self.create_nutrient_analysis(df)
        
        # Machine Learning
        self.create_ml_predictions_section(df)
        
        # Dados brutos
        if show_raw_data:
            st.header("📋 Dados Brutos")
            st.dataframe(df)
        
        # Exportar dados
        self.create_data_export_section(df)
        
        # Footer
        st.markdown("---")
        st.markdown("**FarmTech Solutions v4.0** - Desenvolvido para FIAP | Sistema de Agricultura Digital")
        
        # Auto refresh
        if auto_refresh:
            st.rerun()

# Executar aplicação
if __name__ == "__main__":
    dashboard = FarmTechDashboard()
    dashboard.main()