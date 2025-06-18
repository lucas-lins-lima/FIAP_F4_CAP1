"""
Módulo de Cálculos Agrícolas
Contém funções para cálculos de área, insumos e relatórios
"""

class CalculadoraAgricola:
    """Classe responsável pelos cálculos agrícolas"""
    
    def calcular_areas_totais(self, culturas):
        """Calcula área total por tipo de cultura"""
        print("\n📊 ÁREA TOTAL POR CULTURA")
        print("=" * 50)
        
        if not culturas:
            print("❌ Nenhuma cultura cadastrada!")
            return
        
        # Dicionário para armazenar totais por tipo
        totais = {}
        
        for cultura in culturas:
            tipo = cultura.tipo_cultura
            if tipo not in totais:
                totais[tipo] = {'area': 0, 'quantidade': 0}
            
            totais[tipo]['area'] += cultura.area
            totais[tipo]['quantidade'] += 1
        
        # Exibir resultados
        area_total_geral = 0
        for tipo, dados in totais.items():
            print(f"{self._get_emoji(tipo)} {tipo}:")
            print(f"   Quantidade de plantações: {dados['quantidade']}")
            print(f"   Área total: {dados['area']:.2f} m²")
            print(f"   Área média: {dados['area']/dados['quantidade']:.2f} m²")
            area_total_geral += dados['area']
            print("-" * 50)
        
        print(f"🌍 ÁREA TOTAL GERAL: {area_total_geral:.2f} m²")
    
    def calcular_insumos_totais(self, culturas):
        """Calcula quantidade total de insumos necessários"""
        print("\n🧪 INSUMOS NECESSÁRIOS")
        print("=" * 50)
        
        if not culturas:
            print("❌ Nenhuma cultura cadastrada!")
            return
        
        insumos = {}
        
        for cultura in culturas:
            insumo = cultura.insumo_tipo
            quantidade = cultura.calcular_insumos()
            
            if insumo not in insumos:
                insumos[insumo] = 0
            
            insumos[insumo] += quantidade
        
        custo_total = 0
        for insumo, quantidade in insumos.items():
            custo = self._calcular_custo_insumo(insumo, quantidade)
            custo_total += custo
            
            print(f"💧 {insumo}: {quantidade:.2f} litros")
            print(f"   Custo estimado: R$ {custo:.2f}")
            print("-" * 50)
        
        print(f"💰 CUSTO TOTAL ESTIMADO: R$ {custo_total:.2f}")
    
    def relatorio_completo(self, culturas):
        """Gera relatório completo da fazenda"""
        print("\n📈 RELATÓRIO COMPLETO - FARMTECH SOLUTIONS")
        print("=" * 60)
        
        if not culturas:
            print("❌ Nenhuma cultura cadastrada!")
            return
        
        # Estatísticas gerais
        total_culturas = len(culturas)
        area_total = sum(cultura.area for cultura in culturas)
        
        print(f"📊 RESUMO EXECUTIVO")
        print(f"Total de plantações: {total_culturas}")
        print(f"Área total cultivada: {area_total:.2f} m²")
        print(f"Área média por plantação: {area_total/total_culturas:.2f} m²")
        print("-" * 60)
        
        # Detalhamento por cultura
        self.calcular_areas_totais(culturas)
        print()
        self.calcular_insumos_totais(culturas)
        print()
        
        # Produtividade estimada
        self._calcular_produtividade_estimada(culturas)
    
    def estatisticas_gerais(self, culturas):
        """Calcula estatísticas gerais dos dados"""
        print("\n📊 ESTATÍSTICAS GERAIS")
        print("=" * 50)
        
        if not culturas:
            print("❌ Nenhuma cultura cadastrada!")
            return
        
        areas = [cultura.area for cultura in culturas]
        insumos = [cultura.calcular_insumos() for cultura in culturas]
        
        # Estatísticas de área
        print("📏 ESTATÍSTICAS DE ÁREA:")
        print(f"   Área média: {sum(areas)/len(areas):.2f} m²")
        print(f"   Área mínima: {min(areas):.2f} m²")
        print(f"   Área máxima: {max(areas):.2f} m²")
        print(f"   Desvio padrão: {self._calcular_desvio_padrao(areas):.2f} m²")
        
        print("\n🧪 ESTATÍSTICAS DE INSUMOS:")
        print(f"   Consumo médio: {sum(insumos)/len(insumos):.2f} L")
        print(f"   Consumo mínimo: {min(insumos):.2f} L")
        print(f"   Consumo máximo: {max(insumos):.2f} L")
        print(f"   Desvio padrão: {self._calcular_desvio_padrao(insumos):.2f} L")
    
    def _get_emoji(self, tipo_cultura):
        """Retorna emoji correspondente ao tipo de cultura"""
        emojis = {
            'Café': '☕',
            'Milho': '🌽',
            'Soja': '🫘'
        }
        return emojis.get(tipo_cultura, '🌱')
    
    def _calcular_custo_insumo(self, insumo, quantidade):
        """Calcula custo estimado do insumo (valores fictícios)"""
        precos = {
            'Fosfato': 15.50,    # R$ por litro
            'NPK': 12.30,        # R$ por litro
            'Potássio': 18.90    # R$ por litro
        }
        return precos.get(insumo, 10.0) * quantidade
    
    def _calcular_produtividade_estimada(self, culturas):
        """Calcula produtividade estimada por cultura"""
        print("🌾 PRODUTIVIDADE ESTIMADA")
        print("-" * 50)
        
        # Produtividade média por m² (valores fictícios para exemplo)
        produtividade = {
            'Café': 0.8,      # kg/m²
            'Milho': 1.2,     # kg/m²
            'Soja': 0.9       # kg/m²
        }
        
        producao_total = 0
        for cultura in culturas:
            prod_cultura = cultura.area * produtividade.get(cultura.tipo_cultura, 1.0)
            producao_total += prod_cultura
            print(f"{self._get_emoji(cultura.tipo_cultura)} {cultura.nome}: {prod_cultura:.2f} kg estimados")
        
        print(f"\n🎯 PRODUÇÃO TOTAL ESTIMADA: {producao_total:.2f} kg")
    
    def _calcular_desvio_padrao(self, valores):
        """Calcula desvio padrão de uma lista de valores"""
        if not valores:
            return 0
        
        media = sum(valores) / len(valores)
        variancia = sum((x - media) ** 2 for x in valores) / len(valores)
        return variancia ** 0.5
