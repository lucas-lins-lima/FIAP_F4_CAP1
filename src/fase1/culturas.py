"""
Módulo de Gerenciamento de Culturas
Contém as classes e funções para manipular dados das culturas
"""

import math
from datetime import datetime

class Cultura:
    """Classe base para todas as culturas"""
    
    def __init__(self, nome, proprietario, data_plantio):
        self.nome = nome
        self.proprietario = proprietario
        self.data_plantio = data_plantio
        self.tipo_cultura = ""
        self.area = 0.0
        self.insumo_tipo = ""
        self.insumo_quantidade_por_m2 = 0.0
    
    def calcular_area(self):
        """Método abstrato para calcular área"""
        raise NotImplementedError("Subclasses devem implementar este método")
    
    def calcular_insumos(self):
        """Calcula quantidade total de insumos necessários"""
        return self.area * self.insumo_quantidade_por_m2
    
    def __str__(self):
        return f"{self.tipo_cultura} - {self.nome} ({self.proprietario})"

class Cafe(Cultura):
    """Classe para cultura de café (área circular)"""
    
    def __init__(self, nome, proprietario, data_plantio, raio):
        super().__init__(nome, proprietario, data_plantio)
        self.tipo_cultura = "Café"
        self.raio = raio
        self.insumo_tipo = "Fosfato"
        self.insumo_quantidade_por_m2 = 0.5  # 500ml/m²
        self.area = self.calcular_area()
    
    def calcular_area(self):
        """Calcula área circular (πr²)"""
        return math.pi * (self.raio ** 2)
    
    def __str__(self):
        return f"☕ {super().__str__()} - Raio: {self.raio}m - Área: {self.area:.2f}m²"

class Milho(Cultura):
    """Classe para cultura de milho (área retangular)"""
    
    def __init__(self, nome, proprietario, data_plantio, largura, comprimento):
        super().__init__(nome, proprietario, data_plantio)
        self.tipo_cultura = "Milho"
        self.largura = largura
        self.comprimento = comprimento
        self.insumo_tipo = "NPK"
        self.insumo_quantidade_por_m2 = 0.3  # 300ml/m²
        self.area = self.calcular_area()
    
    def calcular_area(self):
        """Calcula área retangular (L×C)"""
        return self.largura * self.comprimento
    
    def __str__(self):
        return f"🌽 {super().__str__()} - {self.largura}m × {self.comprimento}m - Área: {self.area:.2f}m²"

class Soja(Cultura):
    """Classe para cultura de soja (área retangular)"""
    
    def __init__(self, nome, proprietario, data_plantio, largura, comprimento):
        super().__init__(nome, proprietario, data_plantio)
        self.tipo_cultura = "Soja"
        self.largura = largura
        self.comprimento = comprimento
        self.insumo_tipo = "Potássio"
        self.insumo_quantidade_por_m2 = 0.4  # 400ml/m²
        self.area = self.calcular_area()
    
    def calcular_area(self):
        """Calcula área retangular (L×C)"""
        return self.largura * self.comprimento
    
    def __str__(self):
        return f"🫘 {super().__str__()} - {self.largura}m × {self.comprimento}m - Área: {self.area:.2f}m²"

class GerenciadorCulturas:
    """Classe para gerenciar todas as culturas"""
    
    def __init__(self):
        self.culturas = []
    
    def carregar_dados_exemplo(self):
        """Carrega dados de exemplo para demonstração"""
        self.culturas = [
            Cafe("Fazenda São João", "João Silva", "2024-03-15", 25.0),
            Milho("Plantio Norte", "Maria Santos", "2024-04-01", 100.0, 50.0),
            Soja("Campo Sul", "Pedro Oliveira", "2024-03-20", 80.0, 60.0),
            Cafe("Cafezal Central", "Ana Costa", "2024-02-10", 30.0),
            Milho("Milharal Oeste", "Carlos Lima", "2024-04-15", 120.0, 40.0)
        ]
    
    def adicionar_cafe(self):
        """Adiciona nova cultura de café"""
        try:
            print("\n☕ CADASTRO DE CAFÉ")
            nome = input("Nome da plantação: ")
            proprietario = input("Nome do proprietário: ")
            data_plantio = input("Data de plantio (YYYY-MM-DD): ")
            raio = float(input("Raio da área circular (metros): "))
            
            cafe = Cafe(nome, proprietario, data_plantio, raio)
            self.culturas.append(cafe)
            print(f"✅ Café cadastrado com sucesso! Área: {cafe.area:.2f}m²")
            
        except ValueError:
            print("❌ Erro: Verifique os valores numéricos digitados!")
    
    def adicionar_milho(self):
        """Adiciona nova cultura de milho"""
        try:
            print("\n🌽 CADASTRO DE MILHO")
            nome = input("Nome da plantação: ")
            proprietario = input("Nome do proprietário: ")
            data_plantio = input("Data de plantio (YYYY-MM-DD): ")
            largura = float(input("Largura da área (metros): "))
            comprimento = float(input("Comprimento da área (metros): "))
            
            milho = Milho(nome, proprietario, data_plantio, largura, comprimento)
            self.culturas.append(milho)
            print(f"✅ Milho cadastrado com sucesso! Área: {milho.area:.2f}m²")
            
        except ValueError:
            print("❌ Erro: Verifique os valores numéricos digitados!")
    
    def adicionar_soja(self):
        """Adiciona nova cultura de soja"""
        try:
            print("\n🫘 CADASTRO DE SOJA")
            nome = input("Nome da plantação: ")
            proprietario = input("Nome do proprietário: ")
            data_plantio = input("Data de plantio (YYYY-MM-DD): ")
            largura = float(input("Largura da área (metros): "))
            comprimento = float(input("Comprimento da área (metros): "))
            
            soja = Soja(nome, proprietario, data_plantio, largura, comprimento)
            self.culturas.append(soja)
            print(f"✅ Soja cadastrada com sucesso! Área: {soja.area:.2f}m²")
            
        except ValueError:
            print("❌ Erro: Verifique os valores numéricos digitados!")
    
    def visualizar_dados(self):
        """Visualiza todos os dados cadastrados"""
        print("\n📋 DADOS CADASTRADOS")
        print("=" * 70)
        
        if not self.culturas:
            print("❌ Nenhuma cultura cadastrada!")
            return
        
        for i, cultura in enumerate(self.culturas, 1):
            print(f"{i}. {cultura}")
            print(f"   📅 Plantio: {cultura.data_plantio}")
            print(f"   🧪 Insumo: {cultura.insumo_tipo} - {cultura.calcular_insumos():.2f}L necessários")
            print("-" * 70)
    
    def atualizar_dados(self):
        """Atualiza dados de uma cultura específica"""
        if not self.culturas:
            print("❌ Nenhuma cultura cadastrada!")
            return
        
        print("\n✏️  ATUALIZAR DADOS")
        self.visualizar_dados()
        
        try:
            indice = int(input("\nDigite o número da cultura para atualizar: ")) - 1
            
            if 0 <= indice < len(self.culturas):
                cultura = self.culturas[indice]
                print(f"\nAtualizando: {cultura}")
                
                novo_nome = input(f"Novo nome [{cultura.nome}]: ") or cultura.nome
                novo_proprietario = input(f"Novo proprietário [{cultura.proprietario}]: ") or cultura.proprietario
                
                cultura.nome = novo_nome
                cultura.proprietario = novo_proprietario
                
                print("✅ Dados atualizados com sucesso!")
            else:
                print("❌ Número inválido!")
                
        except ValueError:
            print("❌ Digite um número válido!")
    
    def deletar_dados(self):
        """Deleta uma cultura específica"""
        if not self.culturas:
            print("❌ Nenhuma cultura cadastrada!")
            return
        
        print("\n🗑️  DELETAR DADOS")
        self.visualizar_dados()
        
        try:
            indice = int(input("\nDigite o número da cultura para deletar: ")) - 1
            
            if 0 <= indice < len(self.culturas):
                cultura_removida = self.culturas.pop(indice)
                print(f"✅ {cultura_removida.tipo_cultura} '{cultura_removida.nome}' removida com sucesso!")
            else:
                print("❌ Número inválido!")
                
        except ValueError:
            print("❌ Digite um número válido!")
