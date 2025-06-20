import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from database_manager import FarmTechDatabase
from datetime import datetime, timedelta

class FarmTechAnalysis:
    def __init__(self):
        self.db = FarmTechDatabase()
    
    def generate_sample_data(self, num_records=100):
        """Gera dados de exemplo para análise"""
        print(f"📊 Gerando {num_records} registros de exemplo...")
        
        np.random.seed(42)  # Para reprodutibilidade
        
        for i in range(num_records):
            # Simular variações realistas
            humidity = np.random.normal(45, 15)  # Média 45%, desvio 15%
            humidity = max(10, min(90, humidity))  # Limitar entre 10-90%
            
            ph = np.random.normal(6.8, 0.8)  # pH ideal próximo a 6.8
            ph = max(4.0, min(9.0, ph))  # Limitar entre 4-9
            
            # Nutrientes com probabilidade baseada na "qualidade" do solo
            soil_quality = np.random.random()
            phosphorus = soil_quality > 0.3  # 70% chance de ter fósforo
            potassium = soil_quality > 0.25   # 75% chance de ter potássio
            
            # Bomba baseada em condições
            needs_irrigation = (humidity < 35 or ph < 6.0 or ph > 7.5 or 
                              not phosphorus or not potassium)
            pump_status = needs_irrigation and np.random.random() > 0.1
            
            self.db.insert_sensor_data(humidity, ph, phosphorus, potassium, pump_status)
        
        print("✅ Dados de exemplo gerados com sucesso!")
    
    def analyze_humidity_trends(self):
        """Analisa tendências de umidade"""
        print("\n💧 ANÁLISE DE UMIDADE")
        print("-" * 20)
        
        # Buscar dados
        data = self.db.get_sensor_data(200)
        if not data:
            print("❌ Sem dados para análise!")
            return
        
        humidades = [record['humidity'] for record in data]
        
        # Estatísticas
        media = np.mean(humidades)
        mediana = np.median(humidades)
        desvio = np.std(humidades)
        minimo = np.min(humidades)
        maximo = np.max(humidades)
        
        print(f"📊 Estatísticas de Umidade:")
        print(f"   • Média: {media:.2f}%")
        print(f"   • Mediana: {mediana:.2f}%")
        print(f"   • Desvio Padrão: {desvio:.2f}%")
        print(f"   • Mínimo: {minimo:.2f}%")
        print(f"   • Máximo: {maximo:.2f}%")
        
        # Classificação
        umidade_critica = sum(1 for h in humidades if h < 30)
        umidade_baixa = sum(1 for h in humidades if 30 <= h < 40)
        umidade_ideal = sum(1 for h in humidades if 40 <= h <= 60)
        umidade_alta = sum(1 for h in humidades if h > 60)
        
        total = len(humidades)
        print(f"\n🎯 Classificação da Umidade:")
        print(f"   • Crítica (<30%): {umidade_critica} ({100*umidade_critica/total:.1f}%)")
        print(f"   • Baixa (30-40%): {umidade_baixa} ({100*umidade_baixa/total:.1f}%)")
        print(f"   • Ideal (40-60%): {umidade_ideal} ({100*umidade_ideal/total:.1f}%)")
        print(f"   • Alta (>60%): {umidade_alta} ({100*umidade_alta/total:.1f}%)")
        
        return {
            'media': media,
            'mediana': mediana,
            'desvio': desvio,
            'distribuicao': {
                'critica': umidade_critica,
                'baixa': umidade_baixa,
                'ideal': umidade_ideal,
                'alta': umidade_alta
            }
        }
    
    def analyze_ph_levels(self):
        """Analisa níveis de pH"""
        print("\n🧪 ANÁLISE DE pH")
        print("-" * 13)
        
        data = self.db.get_sensor_data(200)
        if not data:
            print("❌ Sem dados para análise!")
            return
        
        ph_values = [record['ph_level'] for record in data]
        
        # Estatísticas
        media = np.mean(ph_values)
        mediana = np.median(ph_values)
        desvio = np.std(ph_values)
        minimo = np.min(ph_values)
        maximo = np.max(ph_values)
        
        print(f"📊 Estatísticas de pH:")
        print(f"   • Média: {media:.2f}")
        print(f"   • Mediana: {mediana:.2f}")
        print(f"   • Desvio Padrão: {desvio:.2f}")
        print(f"   • Mínimo: {minimo:.2f}")
        print(f"   • Máximo: {maximo:.2f}")
        
        # Classificação do pH
        acido = sum(1 for ph in ph_values if ph < 6.0)
        ideal = sum(1 for ph in ph_values if 6.0 <= ph <= 7.5)
        alcalino = sum(1 for ph in ph_values if ph > 7.5)
        
        total = len(ph_values)
        print(f"\n⚖️ Classificação do pH:")
        print(f"   • Ácido (<6.0): {acido} ({100*acido/total:.1f}%)")
        print(f"   • Ideal (6.0-7.5): {ideal} ({100*ideal/total:.1f}%)")
        print(f"   • Alcalino (>7.5): {alcalino} ({100*alcalino/total:.1f}%)")
        
        return {
            'media': media,
            'mediana': mediana,
            'desvio': desvio,
            'distribuicao': {
                'acido': acido,
                'ideal': ideal,
                'alcalino': alcalino
            }
        }
    
    def analyze_nutrient_availability(self):
        """Analisa disponibilidade de nutrientes"""
        print("\n🌱 ANÁLISE DE NUTRIENTES")
        print("-" * 21)
        
        data = self.db.get_sensor_data(200)
        if not data:
            print("❌ Sem dados para análise!")
            return
        
        fosforo_presente = sum(1 for record in data if record['phosphorus'])
        potassio_presente = sum(1 for record in data if record['potassium'])
        ambos_presentes = sum(1 for record in data if record['phosphorus'] and record['potassium'])
        nenhum_presente = sum(1 for record in data if not record['phosphorus'] and not record['potassium'])
        
        total = len(data)
        
        print(f"📊 Disponibilidade de Nutrientes:")
        print(f"   • Fósforo presente: {fosforo_presente}/{total} ({100*fosforo_presente/total:.1f}%)")
        print(f"   • Potássio presente: {potassio_presente}/{total} ({100*potassio_presente/total:.1f}%)")
        print(f"   • Ambos presentes: {ambos_presentes}/{total} ({100*ambos_presentes/total:.1f}%)")
        print(f"   • Nenhum presente: {nenhum_presente}/{total} ({100*nenhum_presente/total:.1f}%)")
        
        # Recomendações
        if fosforo_presente/total < 0.7:
            print("⚠️ ALERTA: Baixa disponibilidade de fósforo!")
        if potassio_presente/total < 0.7:
            print("⚠️ ALERTA: Baixa disponibilidade de potássio!")
        if ambos_presentes/total < 0.5:
            print("🚨 CRÍTICO: Deficiência nutricional severa!")
        
        return {
            'fosforo_pct': 100*fosforo_presente/total,
            'potassio_pct': 100*potassio_presente/total,
            'ambos_pct': 100*ambos_presentes/total,
            'deficit_pct': 100*nenhum_presente/total
        }
    
    def analyze_irrigation_efficiency(self):
        """Analisa eficiência da irrigação"""
        print("\n💦 ANÁLISE DE IRRIGAÇÃO")
        print("-" * 21)
        
        data = self.db.get_sensor_data(200)
        if not data:
            print("❌ Sem dados para análise!")
            return
        
        total_readings = len(data)
        irrigacao_ativa = sum(1 for record in data if record['pump_status'])
        
        # Analisar contexto da irrigação
        irrigacao_necessaria = 0
        irrigacao_desnecessaria = 0
        
        for record in data:
            needs_water = (record['humidity'] < 35 or 
                          record['ph_level'] < 6.0 or record['ph_level'] > 7.5 or
                          not record['phosphorus'] or not record['potassium'])
            
            if record['pump_status']:
                if needs_water:
                    irrigacao_necessaria += 1
                else:
                    irrigacao_desnecessaria += 1
        
        eficiencia = (irrigacao_necessaria / irrigacao_ativa) * 100 if irrigacao_ativa > 0 else 0
        
        print(f"📊 Estatísticas de Irrigação:")
        print(f"   • Total de leituras: {total_readings}")
        print(f"   • Irrigação ativa: {irrigacao_ativa} ({100*irrigacao_ativa/total_readings:.1f}%)")
        print(f"   • Irrigação necessária: {irrigacao_necessaria}")
        print(f"   • Irrigação desnecessária: {irrigacao_desnecessaria}")
        print(f"   • Eficiência: {eficiencia:.1f}%")
        
        # Recomendações
        if eficiencia < 80:
            print("⚠️ ALERTA: Eficiência da irrigação abaixo do recomendado!")
        elif eficiencia >= 90:
            print("✅ EXCELENTE: Alta eficiência na irrigação!")
        
        return {
            'total_ativacoes': irrigacao_ativa,
            'eficiencia': eficiencia,
            'necessaria': irrigacao_necessaria,
            'desnecessaria': irrigacao_desnecessaria
        }
    
    def generate_comprehensive_report(self):
        """Gera relatório completo do sistema"""
        print("\n" + "="*60)
        print("📋 RELATÓRIO COMPLETO - FARMTECH SOLUTIONS")
        print("="*60)
        
        # Executar todas as análises
        humidity_analysis = self.analyze_humidity_trends()
        ph_analysis = self.analyze_ph_levels()
        nutrient_analysis = self.analyze_nutrient_availability()
        irrigation_analysis = self.analyze_irrigation_efficiency()
        
        # Resumo executivo
        print("\n🎯 RESUMO EXECUTIVO")
        print("-" * 18)
        
        # Status geral do sistema
        status_scores = []
        
        if humidity_analysis:
            if humidity_analysis['distribuicao']['ideal'] > humidity_analysis['distribuicao']['critica']:
                status_scores.append(1)
            else:
                status_scores.append(0)
        
        if ph_analysis:
            if ph_analysis['distribuicao']['ideal'] > (ph_analysis['distribuicao']['acido'] + ph_analysis['distribuicao']['alcalino']):
                status_scores.append(1)
            else:
                status_scores.append(0)
        
        if nutrient_analysis:
            if nutrient_analysis['ambos_pct'] > 50:
                status_scores.append(1)
            else:
                status_scores.append(0)
        
        if irrigation_analysis:
            if irrigation_analysis['eficiencia'] > 80:
                status_scores.append(1)
            else:
                status_scores.append(0)
        
        overall_score = sum(status_scores) / len(status_scores) * 100 if status_scores else 0
        
        print(f"🏆 Score Geral do Sistema: {overall_score:.0f}%")
        
        if overall_score >= 80:
            print("✅ STATUS: Sistema funcionando adequadamente")
        elif overall_score >= 60:
            print("⚠️ STATUS: Sistema necessita ajustes")
        else:
            print("🚨 STATUS: Sistema requer intervenção urgente")
        
        print("\n📊 Próximas ações recomendadas:")
        if humidity_analysis and humidity_analysis['distribuicao']['critica'] > 20:
            print("• Revisar sistema de irrigação")
        if ph_analysis and ph_analysis['distribuicao']['ideal'] < 50:
            print("• Ajustar pH do solo")
        if nutrient_analysis and nutrient_analysis['deficit_pct'] > 30:
            print("• Aplicar fertilizantes")
        if irrigation_analysis and irrigation_analysis['eficiencia'] < 80:
            print("• Otimizar lógica de irrigação")
        
        print("\n" + "="*60)

# Execução principal para testes
if __name__ == "__main__":
    analyzer = FarmTechAnalysis()
    
    # Gerar dados de exemplo se necessário
    stats = analyzer.db.get_statistics()
    if stats['total_readings'] < 50:
        analyzer.generate_sample_data(100)
    
    # Executar relatório completo
    analyzer.generate_comprehensive_report()