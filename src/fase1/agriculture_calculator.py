"""
Módulo de cálculos agrícolas
Responsável pelos cálculos de área e insumos
"""

import math

class AgricultureCalculator:
    """Classe para cálculos relacionados à agricultura"""
    
    def __init__(self):
        """Inicializa o calculador com dados das culturas"""
        self.cultures_data = {
            "Soja": {
                "geometry": "rectangular",
                "input": "Glifosato",
                "dosage": 3.0,  # L/hectare
                "unit": "L"
            },
            "Milho": {
                "geometry": "circular",
                "input": "Ureia",
                "dosage": 200.0,  # kg/hectare
                "unit": "kg"
            },
            "Café": {
                "geometry": "trapezoidal", 
                "input": "Fosfato",
                "dosage": 150.0,  # kg/hectare
                "unit": "kg"
            },
            "Cana-de-açúcar": {
                "geometry": "triangular",
                "input": "NPK Líquido",
                "dosage": 5000.0,  # mL/hectare (500mL/metro convertido)
                "unit": "mL"
            }
        }
    
    def get_available_cultures(self):
        """Retorna lista das culturas disponíveis"""
        return list(self.cultures_data.keys())
    
    def calculate_rectangular_area(self, width, length):
        """Calcula área retangular"""
        return width * length
    
    def calculate_circular_area(self, radius):
        """Calcula área circular"""
        return math.pi * radius ** 2
    
    def calculate_trapezoidal_area(self, major_base, minor_base, height):
        """Calcula área trapezoidal"""
        return ((major_base + minor_base) * height) / 2
    
    def calculate_triangular_area(self, base, height):
        """Calcula área triangular"""
        return (base * height) / 2
    
    def calculate_inputs(self, culture, area_m2):
        """Calcula insumos necessários baseado na área"""
        if culture not in self.cultures_data:
            raise ValueError(f"Cultura '{culture}' não encontrada")
        
        culture_info = self.cultures_data[culture]
        
        # Converter área de m² para hectares
        area_hectares = area_m2 / 10000
        
        # Calcular quantidade de insumo necessária
        total_input = culture_info["dosage"] * area_hectares
        
        return {
            "nome": culture_info["input"],
            "quantidade": total_input,
            "unidade": culture_info["unit"],
            "area_hectares": area_hectares
        }
    
    def get_culture_info(self, culture):
        """Retorna informações completas da cultura"""
        if culture not in self.cultures_data:
            raise ValueError(f"Cultura '{culture}' não encontrada")
        
        return self.cultures_data[culture]