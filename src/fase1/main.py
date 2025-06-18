"""
FarmTech Solutions - Sistema de Gestão Agrícola
Fase 1: Aplicação Python para Agricultura Digital
Autor: Equipe FarmTech Solutions
"""

import os
from culturas import GerenciadorCulturas
from calculos import CalculadoraAgricola

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    """Exibe o menu principal do sistema"""
    print("=" * 50)
    print("🌱 FARMTECH SOLUTIONS - AGRICULTURA DIGITAL 🌱")
    print("=" * 50)
    print("1. 📊 Entrada de Dados")
    print("2. 📋 Visualizar Dados")
    print("3. ✏️  Atualizar Dados")
    print("4. 🗑️  Deletar Dados")
    print("5. 📈 Relatórios e Cálculos")
    print("6. 🚪 Sair do Sistema")
    print("=" * 50)

def menu_entrada_dados(gerenciador):
    """Menu para entrada de novos dados"""
    print("\n📊 ENTRADA DE DADOS")
    print("-" * 30)
    print("1. Café (Área Circular)")
    print("2. Milho (Área Retangular)")
    print("3. Soja (Área Retangular)")
    print("4. Voltar ao Menu Principal")
    
    try:
        opcao = int(input("\nEscolha o tipo de cultura (1-4): "))
        
        if opcao == 1:
            gerenciador.adicionar_cafe()
        elif opcao == 2:
            gerenciador.adicionar_milho()
        elif opcao == 3:
            gerenciador.adicionar_soja()
        elif opcao == 4:
            return
        else:
            print("❌ Opção inválida!")
            
    except ValueError:
        print("❌ Por favor, digite um número válido!")

def menu_relatorios(gerenciador, calculadora):
    """Menu de relatórios e cálculos"""
    print("\n📈 RELATÓRIOS E CÁLCULOS")
    print("-" * 30)
    print("1. Cálculo de Área Total por Cultura")
    print("2. Cálculo de Insumos Necessários")
    print("3. Relatório Completo")
    print("4. Estatísticas Gerais")
    print("5. Voltar ao Menu Principal")
    
    try:
        opcao = int(input("\nEscolha uma opção (1-5): "))
        
        if opcao == 1:
            calculadora.calcular_areas_totais(gerenciador.culturas)
        elif opcao == 2:
            calculadora.calcular_insumos_totais(gerenciador.culturas)
        elif opcao == 3:
            calculadora.relatorio_completo(gerenciador.culturas)
        elif opcao == 4:
            calculadora.estatisticas_gerais(gerenciador.culturas)
        elif opcao == 5:
            return
        else:
            print("❌ Opção inválida!")
            
    except ValueError:
        print("❌ Por favor, digite um número válido!")

def main():
    """Função principal do sistema"""
    gerenciador = GerenciadorCulturas()
    calculadora = CalculadoraAgricola()
    
    # Dados de exemplo para demonstração
    gerenciador.carregar_dados_exemplo()
    
    while True:
        limpar_tela()
        exibir_menu()
        
        try:
            opcao = int(input("\nDigite sua opção (1-6): "))
            
            if opcao == 1:
                menu_entrada_dados(gerenciador)
                
            elif opcao == 2:
                gerenciador.visualizar_dados()
                
            elif opcao == 3:
                gerenciador.atualizar_dados()
                
            elif opcao == 4:
                gerenciador.deletar_dados()
                
            elif opcao == 5:
                menu_relatorios(gerenciador, calculadora)
                
            elif opcao == 6:
                print("\n👋 Obrigado por usar o FarmTech Solutions!")
                print("🌱 Até logo!")
                break
                
            else:
                print("❌ Opção inválida! Tente novamente.")
                
        except ValueError:
            print("❌ Por favor, digite um número válido!")
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário. Até logo!")
            break
        
        input("\n⏸️  Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
