"""
Módulo de gerenciamento de dados
Responsável por armazenar, recuperar e manipular dados das culturas
"""

import json
import os
from datetime import datetime

class DataManager:
    """Classe para gerenciamento de dados das culturas"""
    
    def __init__(self, filename="farmtech_data.json"):
        """Inicializa o gerenciador de dados"""
        self.filename = filename
        self.data = []
        self.filepath = os.path.join(os.path.dirname(__file__), self.filename)
    
    def add_culture_data(self, culture_data):
        """Adiciona dados de uma nova cultura"""
        culture_data["timestamp"] = datetime.now().isoformat()
        culture_data["id"] = len(self.data) + 1
        self.data.append(culture_data)
    
    def get_all_data(self):
        """Retorna todos os dados cadastrados"""
        return self.data.copy()
    
    def update_data(self, index, field, new_value):
        """Atualiza um campo específico de um registro"""
        if 0 <= index < len(self.data):
            self.data[index][field] = new_value
            self.data[index]["last_updated"] = datetime.now().isoformat()
            return True
        return False
    
    def delete_data(self, index):
        """Remove um registro específico"""
        if 0 <= index < len(self.data):
            del self.data[index]
            # Reindexar IDs
            for i, item in enumerate(self.data):
                item["id"] = i + 1
            return True
        return False
    
    def save_data(self):
        """Salva dados em arquivo JSON"""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {str(e)}")
            return False
    
    def load_data(self):
        """Carrega dados do arquivo JSON"""
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                return True
            else:
                self.data = []
                return True
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            self.data = []
            return False
    
    def get_statistics(self):
        """Calcula estatísticas básicas dos dados"""
        if not self.data:
            return None
        
        areas = [item["area"] for item in self.data]
        culturas = [item["cultura"] for item in self.data]
        
        # Contar culturas únicas
        culturas_unicas = list(set(culturas))
        distribuicao_culturas = {}
        for cultura in culturas:
            distribuicao_culturas[cultura] = distribuicao_culturas.get(cultura, 0) + 1
        
        return {
            "total_registros": len(self.data),
            "culturas_unicas": culturas_unicas,
            "area_total": sum(areas),
            "area_media": sum(areas) / len(areas),
            "area_maxima": max(areas),
            "area_minima": min(areas),
            "distribuicao_culturas": distribuicao_culturas
        }
    
    def export_to_r_format(self, output_file="data_for_r.csv"):
        """Exporta dados em formato CSV para análise em R"""
        try:
            import csv
            
            if not self.data:
                return False
            
            output_path = os.path.join(os.path.dirname(__file__), output_file)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'nome_area', 'cultura', 'area', 'insumo_nome', 
                             'insumo_quantidade', 'insumo_unidade', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for item in self.data:
                    writer.writerow({
                        'id': item['id'],
                        'nome_area': item['nome_area'],
                        'cultura': item['cultura'],
                        'area': item['area'],
                        'insumo_nome': item['insumos']['nome'],
                        'insumo_quantidade': item['insumos']['quantidade'],
                        'insumo_unidade': item['insumos']['unidade'],
                        'timestamp': item['timestamp']
                    })
            
            return True
        except Exception as e:
            print(f"Erro ao exportar para R: {str(e)}")
            return False