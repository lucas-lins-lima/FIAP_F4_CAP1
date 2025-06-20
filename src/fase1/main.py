#!/usr/bin/env python3
"""
FarmTech Solutions - Sistema de Gestão Agrícola
Fase 1: Cálculos de área e manejo de insumos

Desenvolvido para FIAP - Agricultura Digital
Autor: Equipe FarmTech Solutions
Data: Dezembro 2024
"""

import os
import sys
from agriculture_calculator import AgricultureCalculator
from data_manager import DataManager

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Exibe o cabeçalho do sistema"""
    print("=" * 60)
    print("🌾 FARMTECH SOLUTIONS - AGRICULTURA DIGITAL 🌾")
    print("=" * 60)
    print("Sistema de Gestão Agrícola - Fase 1")
    print("FIAP - Faculdade de Informática e Administração Paulista")
    print("=" * 60)

def print_menu():
    """Exibe o menu principal"""
    print("\n📋 MENU PRINCIPAL")
    print("-" * 30)
    print("1. 📊 Entrada de Dados")
    print("2. 📋 Visualizar Dados")
    print("3. ✏️  Atualizar Dados")
    print("4. 🗑️  Deletar Dados")
    print("5. 📈 Relatório Estatístico")
    print("6. 🎲 Gerar Dados Demonstração")
    print("7. 💾 Salvar Dados")
    print("8. 📂 Carregar Dados")
    print("9. 🌱 Ver Culturas Disponíveis")
    print("0. 🚪 Sair do Sistema")
    print("-" * 30)

def main():
    """Função principal do sistema"""
    calculator = AgricultureCalculator()
    data_manager = DataManager()
    
    # Carregar dados salvos anteriormente (se existirem)
    data_manager.load_data()
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        # Mostrar status dos dados
        dados_count = len(data_manager.get_all_data())
        print(f"\n📊 Status: {dados_count} registro(s) cadastrado(s)")
        
        try:
            opcao = input("\n🔸 Escolha uma opção: ").strip()
            
            if opcao == '1':
                entrada_dados(calculator, data_manager)
            elif opcao == '2':
                visualizar_dados(data_manager)
            elif opcao == '3':
                atualizar_dados(data_manager)
            elif opcao == '4':
                deletar_dados(data_manager)
            elif opcao == '5':
                relatorio_estatistico(data_manager)
            elif opcao == '6':
                gerar_dados_demo(calculator, data_manager)
            elif opcao == '7':
                data_manager.save_data()
                print("\n✅ Dados salvos com sucesso!")
                input("\nPressione ENTER para continuar...")
            elif opcao == '8':
                data_manager.load_data()
                print("\n✅ Dados carregados com sucesso!")
                input("\nPressione ENTER para continuar...")
            elif opcao == '9':
                mostrar_culturas_disponiveis(calculator)
            elif opcao == '0':
                print("\n👋 Obrigado por usar o FarmTech Solutions!")
                print("🌱 Até logo!")
                sys.exit(0)
            else:
                print("\n❌ Opção inválida! Tente novamente.")
                input("\nPressione ENTER para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")
            input("\nPressione ENTER para continuar...")

def mostrar_culturas_disponiveis(calculator):
    """Mostra informações das culturas disponíveis"""
    clear_screen()
    print_header()
    print("\n🌱 CULTURAS DISPONÍVEIS NO SISTEMA")
    print("-" * 45)
    
    culturas = calculator.get_available_cultures()
    
    for cultura in culturas:
        info = calculator.get_culture_info(cultura)
        print(f"\n🌾 {cultura}:")
        print(f"   📐 Geometria: {info['geometry']}")
        print(f"   🧪 Insumo: {info['input']}")
        print(f"   📊 Dosagem: {info['dosage']} {info['unit']}/hectare")
    
    print(f"\n💡 Para cadastrar dados reais, use a opção '1. Entrada de Dados'")
    print(f"💡 Para dados de teste, use a opção '6. Gerar Dados Demonstração'")
    
    input("\nPressione ENTER para continuar...")

def gerar_dados_demo(calculator, data_manager):
    """Gera dados de demonstração"""
    clear_screen()
    print_header()
    print("\n🎲 GERANDO DADOS DE DEMONSTRAÇÃO")
    print("-" * 35)
    
    dados_demo = [
        {
            "nome_area": "Fazenda São João - Lote A",
            "cultura": "Soja",
            "dimensoes": {"largura": 200, "comprimento": 300},
            "area": 60000,
            "insumos": calculator.calculate_inputs("Soja", 60000)
        },
        {
            "nome_area": "Propriedade Rural Esperança",
            "cultura": "Milho", 
            "dimensoes": {"raio": 150},
            "area": 70686,
            "insumos": calculator.calculate_inputs("Milho", 70686)
        },
        {
            "nome_area": "Cafezal Monte Verde",
            "cultura": "Café",
            "dimensoes": {"base_maior": 250, "base_menor": 180, "altura": 200},
            "area": 43000,
            "insumos": calculator.calculate_inputs("Café", 43000)
        },
        {
            "nome_area": "Usina Doce Vida - Setor B",
            "cultura": "Cana-de-açúcar",
            "dimensoes": {"base": 400, "altura": 300},
            "area": 60000,
            "insumos": calculator.calculate_inputs("Cana-de-açúcar", 60000)
        }
    ]
    
    for dados in dados_demo:
        data_manager.add_culture_data(dados)
    
    print("✅ Dados de demonstração gerados com sucesso!")
    print(f"📊 {len(dados_demo)} registros adicionados")
    print("\n📋 Dados gerados:")
    for dados in dados_demo:
        print(f"   • {dados['nome_area']} - {dados['cultura']}")
    
    input("\nPressione ENTER para continuar...")

def entrada_dados(calculator, data_manager):
    """Gerencia a entrada de dados das culturas"""
    clear_screen()
    print_header()
    print("\n📊 ENTRADA DE DADOS - NOVA CULTURA")
    print("-" * 40)
    
    # Mostrar culturas disponíveis
    culturas = calculator.get_available_cultures()
    print("\n🌱 Culturas Disponíveis:")
    for i, cultura in enumerate(culturas, 1):
        info = calculator.get_culture_info(cultura)
        print(f"{i}. {cultura} (Geometria: {info['geometry']}, Insumo: {info['input']})")
    
    try:
        cultura_idx = int(input("\n🔸 Escolha a cultura (número): ")) - 1
        if cultura_idx < 0 or cultura_idx >= len(culturas):
            raise ValueError("Cultura inválida")
        
        cultura_escolhida = culturas[cultura_idx]
        print(f"\n✅ Cultura selecionada: {cultura_escolhida}")
        
        # Coletar dados específicos da cultura
        dados = coletar_dados_cultura(cultura_escolhida, calculator)
        
        # Adicionar aos dados gerenciados
        data_manager.add_culture_data(dados)
        
        print(f"\n✅ Dados da cultura {cultura_escolhida} adicionados com sucesso!")
        
    except (ValueError, IndexError) as e:
        print(f"\n❌ Erro na entrada de dados: {str(e)}")
    
    input("\nPressione ENTER para continuar...")

def coletar_dados_cultura(cultura, calculator):
    """Coleta dados específicos de cada cultura"""
    print(f"\n📝 Coletando dados para: {cultura}")
    print("-" * 30)
    
    # Nome da área/propriedade
    nome_area = input("🏷️  Nome da área/propriedade: ").strip()
    
    # Dados baseados na geometria da cultura
    if cultura == "Soja":
        print("📐 Geometria: Retangular")
        largura = float(input("📏 Largura do terreno (metros): "))
        comprimento = float(input("📏 Comprimento do terreno (metros): "))
        area = calculator.calculate_rectangular_area(largura, comprimento)
        dimensoes = {"largura": largura, "comprimento": comprimento}
        
    elif cultura == "Milho":
        print("📐 Geometria: Circular (Pivô)")
        raio = float(input("📏 Raio do pivô (metros): "))
        area = calculator.calculate_circular_area(raio)
        dimensoes = {"raio": raio}
        
    elif cultura == "Café":
        print("📐 Geometria: Trapezoidal")
        base_maior = float(input("📏 Base maior do trapézio (metros): "))
        base_menor = float(input("📏 Base menor do trapézio (metros): "))
        altura = float(input("📏 Altura do trapézio (metros): "))
        area = calculator.calculate_trapezoidal_area(base_maior, base_menor, altura)
        dimensoes = {"base_maior": base_maior, "base_menor": base_menor, "altura": altura}
        
    elif cultura == "Cana-de-açúcar":
        print("📐 Geometria: Triangular")
        base = float(input("📏 Base do triângulo (metros): "))
        altura = float(input("📏 Altura do triângulo (metros): "))
        area = calculator.calculate_triangular_area(base, altura)
        dimensoes = {"base": base, "altura": altura}
    
    # Calcular insumos necessários
    insumos = calculator.calculate_inputs(cultura, area)
    
    # Mostrar resumo
    print(f"\n📊 RESUMO DO CADASTRO:")
    print(f"   📍 Área: {nome_area}")
    print(f"   🌾 Cultura: {cultura}")
    print(f"   📐 Área total: {area:.2f} m² ({area/10000:.4f} hectares)")
    print(f"   🧪 Insumo necessário: {insumos['quantidade']:.2f} {insumos['unidade']}")
    
    return {
        "nome_area": nome_area,
        "cultura": cultura,
        "dimensoes": dimensoes,
        "area": area,
        "insumos": insumos
    }

def visualizar_dados(data_manager):
    """Visualiza todos os dados cadastrados"""
    clear_screen()
    print_header()
    print("\n📋 DADOS CADASTRADOS")
    print("-" * 40)
    
    dados = data_manager.get_all_data()
    
    if not dados:
        print("\n❌ Nenhum dado cadastrado ainda.")
        print("\n💡 DICAS:")
        print("   • Use a opção '1' para cadastrar dados manualmente")
        print("   • Use a opção '6' para gerar dados de demonstração")
        print("   • Use a opção '9' para ver as culturas disponíveis")
    else:
        for i, item in enumerate(dados, 1):
            print(f"\n🌱 Registro #{i}")
            print(f"   📍 Área: {item['nome_area']}")
            print(f"   🌾 Cultura: {item['cultura']}")
            print(f"   📐 Área total: {item['area']:.2f} m² ({item['area']/10000:.4f} hectares)")
            print(f"   🧪 Insumo: {item['insumos']['nome']}")
            print(f"   📊 Quantidade: {item['insumos']['quantidade']:.2f} {item['insumos']['unidade']}")
            print("-" * 30)
        
        # Exportar para R se houver dados
        if data_manager.export_to_r_format():
            print(f"\n✅ Dados exportados para 'data_for_r.csv' (análise em R)")
    
    input("\nPressione ENTER para continuar...")

def atualizar_dados(data_manager):
    """Atualiza dados de uma posição específica"""
    clear_screen()
    print_header()
    print("\n✏️ ATUALIZAR DADOS")
    print("-" * 25)
    
    dados = data_manager.get_all_data()
    
    if not dados:
        print("\n❌ Nenhum dado cadastrado para atualizar.")
        input("\nPressione ENTER para continuar...")
        return
    
    # Mostrar dados existentes
    print("\n📋 Registros disponíveis:")
    for i, item in enumerate(dados, 1):
        print(f"{i}. {item['nome_area']} - {item['cultura']}")
    
    try:
        indice = int(input("\n🔸 Número do registro para atualizar: ")) - 1
        
        if 0 <= indice < len(dados):
            # Aqui você pode implementar a lógica de atualização
            novo_nome = input(f"🏷️  Novo nome da área (atual: {dados[indice]['nome_area']}): ").strip()
            if novo_nome:
                data_manager.update_data(indice, "nome_area", novo_nome)
                print("\n✅ Dados atualizados com sucesso!")
            else:
                print("\n❌ Nenhuma alteração realizada.")
        else:
            print("\n❌ Registro não encontrado.")
            
    except (ValueError, IndexError):
        print("\n❌ Entrada inválida.")
    
    input("\nPressione ENTER para continuar...")

def deletar_dados(data_manager):
    """Deleta dados de uma posição específica"""
    clear_screen()
    print_header()
    print("\n🗑️ DELETAR DADOS")
    print("-" * 20)
    
    dados = data_manager.get_all_data()
    
    if not dados:
        print("\n❌ Nenhum dado cadastrado para deletar.")
        input("\nPressione ENTER para continuar...")
        return
    
    # Mostrar dados existentes
    print("\n📋 Registros disponíveis:")
    for i, item in enumerate(dados, 1):
        print(f"{i}. {item['nome_area']} - {item['cultura']}")
    
    try:
        indice = int(input("\n🔸 Número do registro para deletar: ")) - 1
        
        if 0 <= indice < len(dados):
            confirmacao = input(f"\n⚠️ Confirma a exclusão de '{dados[indice]['nome_area']}'? (s/N): ").lower()
            if confirmacao == 's':
                data_manager.delete_data(indice)
                print("\n✅ Registro deletado com sucesso!")
            else:
                print("\n❌ Operação cancelada.")
        else:
            print("\n❌ Registro não encontrado.")
            
    except (ValueError, IndexError):
        print("\n❌ Entrada inválida.")
    
    input("\nPressione ENTER para continuar...")

def relatorio_estatistico(data_manager):
    """Gera relatório estatístico dos dados"""
    clear_screen()
    print_header()
    print("\n📈 RELATÓRIO ESTATÍSTICO")
    print("-" * 30)
    
    stats = data_manager.get_statistics()
    
    if not stats:
        print("\n❌ Dados insuficientes para gerar estatísticas.")
        print("\n💡 Cadastre pelo menos um registro para ver estatísticas.")
    else:
        print(f"\n📊 Total de registros: {stats['total_registros']}")
        print(f"🌾 Culturas cadastradas: {', '.join(stats['culturas_unicas'])}")
        print(f"📐 Área total: {stats['area_total']:.2f} m² ({stats['area_total']/10000:.4f} hectares)")
        print(f"📐 Área média: {stats['area_media']:.2f} m²")
        print(f"📐 Maior área: {stats['area_maxima']:.2f} m²")
        print(f"📐 Menor área: {stats['area_minima']:.2f} m²")
        
        print("\n🧪 Distribuição por cultura:")
        for cultura, count in stats['distribuicao_culturas'].items():
            print(f"   {cultura}: {count} registro(s)")
    
    input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()