import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging
from dataclasses import dataclass
import os
from database_enhanced import EnhancedFarmTechDatabase

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    precipitation: float
    weather_condition: str
    timestamp: datetime
    forecast_hours: int = 0

class WeatherAPIClient:
    def __init__(self, api_key: str = None):
        # API Key do OpenWeatherMap (substitua pela sua chave real)
        self.api_key = api_key or "YOUR_OPENWEATHER_API_KEY"
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.db = EnhancedFarmTechDatabase()
        
    def get_current_weather(self, city: str = "São Paulo", country: str = "BR") -> Optional[WeatherData]:
        """Obtém dados meteorológicos atuais"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{city},{country}",
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            weather_data = WeatherData(
                temperature=data['main']['temp'],
                humidity=data['main']['humidity'],
                pressure=data['main']['pressure'],
                wind_speed=data['wind'].get('speed', 0),
                precipitation=data.get('rain', {}).get('1h', 0),
                weather_condition=data['weather'][0]['description'],
                timestamp=datetime.now()
            )
            
            # Salvar no banco de dados
            self._save_weather_data(weather_data, "current")
            
            logger.info(f"🌤️ Dados meteorológicos atuais obtidos para {city}")
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro ao obter dados meteorológicos: {e}")
            return None
        except KeyError as e:
            logger.error(f"❌ Formato de resposta inesperado: {e}")
            return None
    
    def get_weather_forecast(self, city: str = "São Paulo", country: str = "BR", 
                           hours: int = 24) -> List[WeatherData]:
        """Obtém previsão meteorológica"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': f"{city},{country}",
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecasts = []
            
            for i, forecast in enumerate(data['list'][:hours//3]):  # Dados a cada 3 horas
                weather_data = WeatherData(
                    temperature=forecast['main']['temp'],
                    humidity=forecast['main']['humidity'],
                    pressure=forecast['main']['pressure'],
                    wind_speed=forecast['wind'].get('speed', 0),
                    precipitation=forecast.get('rain', {}).get('3h', 0),
                    weather_condition=forecast['weather'][0]['description'],
                    timestamp=datetime.fromtimestamp(forecast['dt']),
                    forecast_hours=(i + 1) * 3
                )
                
                forecasts.append(weather_data)
                # Salvar no banco
                self._save_weather_data(weather_data, "forecast")
            
            logger.info(f"🌦️ Previsão meteorológica obtida para {city} ({len(forecasts)} períodos)")
            return forecasts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erro ao obter previsão meteorológica: {e}")
            return []
    
    def _save_weather_data(self, weather: WeatherData, data_source: str):
        """Salva dados meteorológicos no banco"""
        try:
            conn = self.db._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO weather_data 
                (temperature, humidity, pressure, wind_speed, precipitation, 
                 weather_condition, forecast_hours, data_source, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                weather.temperature, weather.humidity, weather.pressure,
                weather.wind_speed, weather.precipitation, weather.weather_condition,
                weather.forecast_hours, data_source, weather.timestamp
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar dados meteorológicos: {e}")

class SmartIrrigationDecision:
    def __init__(self):
        self.weather_client = WeatherAPIClient()
        self.db = EnhancedFarmTechDatabase()
        
    def make_irrigation_decision(self, current_humidity: float, current_ph: float,
                               phosphorus: bool, potassium: bool) -> Dict:
        """Toma decisão inteligente de irrigação considerando dados meteorológicos"""
        
        # Obter dados meteorológicos atuais
        current_weather = self.weather_client.get_current_weather()
        forecast = self.weather_client.get_weather_forecast(hours=12)
        
        # Decisão baseada apenas nos sensores
        sensor_based_decision = self._sensor_based_decision(
            current_humidity, current_ph, phosphorus, potassium
        )
        
        # Ajustar decisão com dados meteorológicos
        weather_adjusted_decision = self._weather_adjusted_decision(
            sensor_based_decision, current_weather, forecast
        )
        
        # Calcular economia de água potencial
        water_savings = self._calculate_water_savings(
            sensor_based_decision, weather_adjusted_decision
        )
        
        return {
            'irrigation_recommended': weather_adjusted_decision['irrigate'],
            'confidence': weather_adjusted_decision['confidence'],
            'reasoning': weather_adjusted_decision['reasons'],
            'sensor_only_decision': sensor_based_decision['irrigate'],
            'weather_influence': weather_adjusted_decision['weather_influence'],
            'water_savings_liters': water_savings,
            'current_weather': self._format_weather_data(current_weather),
            'precipitation_forecast': self._get_precipitation_forecast(forecast),
            'decision_timestamp': datetime.now().isoformat()
        }
    
    def _sensor_based_decision(self, humidity: float, ph: float, 
                             phosphorus: bool, potassium: bool) -> Dict:
        """Decisão baseada apenas nos sensores"""
        reasons = []
        should_irrigate = False
        confidence = 0.5
        
        # Verificar umidade
        if humidity < 25:
            should_irrigate = True
            reasons.append(f"Umidade crítica ({humidity:.1f}%)")
            confidence += 0.3
        elif humidity < 35:
            should_irrigate = True
            reasons.append(f"Umidade baixa ({humidity:.1f}%)")
            confidence += 0.2
        elif humidity > 65:
            reasons.append(f"Umidade adequada ({humidity:.1f}%)")
            confidence -= 0.1
        
        # Verificar pH
        if ph < 6.0 or ph > 7.5:
            should_irrigate = True
            reasons.append(f"pH inadequado ({ph:.2f})")
            confidence += 0.15
        
        # Verificar nutrientes
        if not phosphorus:
            should_irrigate = True
            reasons.append("Fósforo insuficiente")
            confidence += 0.1
        
        if not potassium:
            should_irrigate = True
            reasons.append("Potássio insuficiente")
            confidence += 0.1
        
        confidence = min(1.0, max(0.0, confidence))
        
        return {
            'irrigate': should_irrigate,
            'confidence': confidence,
            'reasons': reasons
        }
    
    def _weather_adjusted_decision(self, sensor_decision: Dict, 
                                 current_weather: Optional[WeatherData],
                                 forecast: List[WeatherData]) -> Dict:
        """Ajusta decisão com base nos dados meteorológicos"""
        
        decision = sensor_decision.copy()
        weather_reasons = []
        weather_influence = 0
        
        if not current_weather:
            decision['weather_influence'] = 0
            decision['reasons'].append("Dados meteorológicos indisponíveis")
            return decision
        
        # Verificar chuva atual
        if current_weather.precipitation > 0:
            if decision['irrigate']:
                decision['irrigate'] = False
                decision['confidence'] = 0.9
                weather_reasons.append(f"Chuva atual ({current_weather.precipitation:.1f}mm)")
                weather_influence = -0.8
        
        # Verificar previsão de chuva
        rain_forecast = sum(f.precipitation for f in forecast[:4])  # Próximas 12 horas
        if rain_forecast > 5:  # Mais de 5mm previstos
            if decision['irrigate']:
                decision['irrigate'] = False
                decision['confidence'] = 0.85
                weather_reasons.append(f"Chuva prevista ({rain_forecast:.1f}mm)")
                weather_influence = -0.6
        
        # Verificar temperatura alta
        if current_weather.temperature > 32:
            if not decision['irrigate'] and sensor_decision['confidence'] < 0.7:
                decision['irrigate'] = True
                decision['confidence'] = 0.75
                weather_reasons.append(f"Temperatura alta ({current_weather.temperature:.1f}°C)")
                weather_influence = 0.4
        
        # Verificar umidade atmosférica
        if current_weather.humidity > 80:
            weather_reasons.append("Alta umidade atmosférica - irrigação menos eficiente")
            if decision['irrigate']:
                decision['confidence'] *= 0.8
                weather_influence -= 0.2
        
        # Verificar vento forte
        if current_weather.wind_speed > 15:  # km/h
            weather_reasons.append("Vento forte - possível perda de água por evaporação")
            if decision['irrigate']:
                decision['confidence'] *= 0.9
                weather_influence -= 0.1
        
        decision['reasons'].extend(weather_reasons)
        decision['weather_influence'] = weather_influence
        
        return decision
    
    def _calculate_water_savings(self, sensor_decision: Dict, 
                               weather_decision: Dict) -> float:
        """Calcula economia de água em litros"""
        base_irrigation_amount = 50  # litros base por irrigação
        
        if sensor_decision['irrigate'] and not weather_decision['irrigate']:
            # Economizou água evitando irrigação desnecessária
            return base_irrigation_amount
        elif not sensor_decision['irrigate'] and weather_decision['irrigate']:
            # Gastará água extra devido ao clima
            return -base_irrigation_amount * 0.3
        
        return 0
    
    def _format_weather_data(self, weather: Optional[WeatherData]) -> Optional[Dict]:
        """Formata dados meteorológicos para resposta"""
        if not weather:
            return None
        
        return {
            'temperature': weather.temperature,
            'humidity': weather.humidity,
            'pressure': weather.pressure,
            'wind_speed': weather.wind_speed,
            'precipitation': weather.precipitation,
            'condition': weather.weather_condition,
            'timestamp': weather.timestamp.isoformat()
        }
    
    def _get_precipitation_forecast(self, forecast: List[WeatherData]) -> Dict:
        """Analisa previsão de precipitação"""
        if not forecast:
            return {'total': 0, 'periods': []}
        
        total_rain = sum(f.precipitation for f in forecast)
        periods = []
        
        for f in forecast:
            if f.precipitation > 0:
                periods.append({
                    'time': f.timestamp.isoformat(),
                    'precipitation': f.precipitation,
                    'hours_ahead': f.forecast_hours
                })
        
        return {
            'total_mm': total_rain,
            'periods_with_rain': len(periods),
            'periods': periods
        }

# Exemplo de uso e teste
if __name__ == "__main__":
    # Testar cliente de clima
    weather_client = WeatherAPIClient()
    
    print("🌤️ Testando API meteorológica...")
    current = weather_client.get_current_weather("São Paulo", "BR")
    
    if current:
        print(f"Temperatura: {current.temperature}°C")
        print(f"Umidade: {current.humidity}%")
        print(f"Condição: {current.weather_condition}")
        print(f"Precipitação: {current.precipitation}mm")
    
    # Testar decisão inteligente
    print("\n🧠 Testando decisão inteligente de irrigação...")
    smart_decision = SmartIrrigationDecision()
    
    # Cenários de teste
    test_scenarios = [
        {
            'name': 'Solo seco',
            'humidity': 25,
            'ph': 6.5,
            'phosphorus': True,
            'potassium': True
        },
        {
            'name': 'Condições ideais',
            'humidity': 55,
            'ph': 6.8,
            'phosphorus': True,
            'potassium': True
        },
        {
            'name': 'Nutrientes baixos',
            'humidity': 45,
            'ph': 6.0,
            'phosphorus': False,
            'potassium': False
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📊 Cenário: {scenario['name']}")
        decision = smart_decision.make_irrigation_decision(
            scenario['humidity'],
            scenario['ph'],
            scenario['phosphorus'],
            scenario['potassium']
        )
        
        print(f"Irrigar: {'✅ SIM' if decision['irrigation_recommended'] else '❌ NÃO'}")
        print(f"Confiança: {decision['confidence']:.1%}")
        print(f"Motivos: {', '.join(decision['reasoning'])}")
        if decision['water_savings_liters'] != 0:
            savings_text = "economia" if decision['water_savings_liters'] > 0 else "gasto extra"
            print(f"Água: {abs(decision['water_savings_liters']):.1f}L {savings_text}")