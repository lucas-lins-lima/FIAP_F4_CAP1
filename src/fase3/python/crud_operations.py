from database_manager import FarmTechDatabase
from datetime import datetime, timedelta
import json

class FarmTechCRUD:
    def __init__(self):
        self.db = FarmTechDatabase()
        
    def menu_principal(self):
        """Menu principal do sistema CRUD"""
        while True:
            print("\n" + "="*50)
            print("🌾 FARMTECH SOLUTIONS - SISTEMA CRUD")
            print("="*50)
            print("1. 📊 Inserir dados de sensores")
            print("2. 📋 Consultar dados")
            print("3. ✏️  Atualizar registro")
            print("4. 🗑️  Deletar registro")
            print("5. 📈 Estatísticas do sistema")
            print("6. 🔍 Buscar por período")
            print("7. 💾 Exportar dados")
            print("8. 🚪 Sair")
            print("="*50)
            
            opcao = input("Digite sua opção: ").strip()
            
            if opcao == "1":
                self.inserir_dados()
            elif opcao == "2":
                self.consultar_dados()
            elif opcao == "3":
                self.atualizar_registro()
            elif opcao == "4":
                self.deletar_registro()
            elif opcao == "5":
                self.mostrar_estatisticas()
            elif opcao == "6":
                self.buscar_por_periodo()
            elif opcao == "7":
                self.exportar_dados()
            elif opcao == "8":
                print("👋 Saindo do sistema...")
                break
            else:
                print("❌ Opção inválida!")
    
    def inserir_dados(self):
        """Inserção manual de dados dos sensores"""
        print("\n📊 INSERIR DADOS DOS SENSORES")
        print("-" * 30)
        
        try:
            # Coleta dos dados
            humidity = float(input("Umidade do solo (%): "))
            ph = float(input("Nível de pH (0-14): "))
            
            print("\nFósforo presente? (s/n): ", end="")
            phosphorus = input().lower().strip() == 's'
            
            print("Potássio presente? (s/n): ", end="")
            potassium = input().lower().strip() == 's'
            
            print("Bomba ativa? (s/n): ", end="")
            pump_status = input().lower().strip() == 's'
            
            # Validações
            if not (0 <= humidity <= 100):
                print("❌ Umidade deve estar entre 0 e 100%")
                return
                
            if not (0 <= ph <= 14):
                print("❌ pH deve estar entre 0 e 14")
                return
            
            # Inserção no banco
            record_id = self.db.insert_sensor_data(humidity, ph, phosphorus, potassium, pump_status)
            
            print(f"✅ Dados inseridos com sucesso! ID do registro: {record_id}")
            
            # Mostrar o registro inserido
            self.mostrar_registro(record_id)
            
        except ValueError:
            print("❌ Erro: Digite valores numéricos válidos para umidade e pH")
        except Exception as e:
            print(f"❌ Erro ao inserir dados: {e}")
    
    def consultar_dados(self):
        """Consulta dados com opções de filtro"""
        print("\n📋 CONSULTAR DADOS")
        print("-" * 20)
        print("1. Últimos 10 registros")
        print("2. Últimos 50 registros")
        print("3. Todos os registros")
        print("4. Buscar por ID")
        
        opcao = input("Digite sua opção: ").strip()
        
        try:
            if opcao == "1":
                dados = self.db.get_sensor_data(10)
            elif opcao == "2":
                dados = self.db.get_sensor_data(50)
            elif opcao == "3":
                dados = self.db.get_sensor_data(1000)
            elif opcao == "4":
                record_id = int(input("Digite o ID do registro: "))
                dados = [self.buscar_por_id(record_id)]
                if dados[0] is None:
                    print("❌ Registro não encontrado!")
                    return
            else:
                print("❌ Opção inválida!")
                return
            
            if not dados:
                print("📭 Nenhum registro encontrado!")
                return
            
            self.exibir_tabela_dados(dados)
            
        except ValueError:
            print("❌ Digite um número válido!")
        except Exception as e:
            print(f"❌ Erro ao consultar dados: {e}")
    
    def atualizar_registro(self):
        """Atualiza um registro específico"""
        print("\n✏️ ATUALIZAR REGISTRO")
        print("-" * 20)
        
        try:
            record_id = int(input("Digite o ID do registro a ser atualizado: "))
            
            # Verificar se o registro existe
            registro_atual = self.buscar_por_id(record_id)
            if not registro_atual:
                print("❌ Registro não encontrado!")
                return
            
            print("\nRegistro atual:")
            self.exibir_tabela_dados([registro_atual])
            
            print("\n📝 Digite os novos valores (Enter para manter o atual):")
            
            # Coleta dos novos dados
            updates = {}
            
            nova_umidade = input(f"Umidade atual: {registro_atual['humidity']}% - Nova umidade: ").strip()
            if nova_umidade:
                updates['humidity'] = float(nova_umidade)
            
            novo_ph = input(f"pH atual: {registro_atual['ph_level']} - Novo pH: ").strip()
            if novo_ph:
                updates['ph_level'] = float(novo_ph)
            
            novo_fosforo = input(f"Fósforo atual: {'Sim' if registro_atual['phosphorus'] else 'Não'} - Novo (s/n): ").strip()
            if novo_fosforo:
                updates['phosphorus'] = novo_fosforo.lower() == 's'
            
            novo_potassio = input(f"Potássio atual: {'Sim' if registro_atual['potassium'] else 'Não'} - Novo (s/n): ").strip()
            if novo_potassio:
                updates['potassium'] = novo_potassio.lower() == 's'
            
            nova_bomba = input(f"Bomba atual: {'Ligada' if registro_atual['pump_status'] else 'Desligada'} - Nova (s/n): ").strip()
            if nova_bomba:
                updates['pump_status'] = nova_bomba.lower() == 's'
            
            if not updates:
                print("ℹ️ Nenhuma alteração foi feita.")
                return
            
            # Realizar a atualização
            if self.db.update_sensor_data(record_id, **updates):
                print("✅ Registro atualizado com sucesso!")
                self.mostrar_registro(record_id)
            else:
                print("❌ Erro ao atualizar registro!")
                
        except ValueError:
            print("❌ Digite valores válidos!")
        except Exception as e:
            print(f"❌ Erro ao atualizar registro: {e}")
    
    def deletar_registro(self):
        """Deleta um registro específico"""
        print("\n🗑️ DELETAR REGISTRO")
        print("-" * 18)
        
        try:
            record_id = int(input("Digite o ID do registro a ser deletado: "))
            
            # Verificar se o registro existe
            registro = self.buscar_por_id(record_id)
            if not registro:
                print("❌ Registro não encontrado!")
                return
            
            print("\nRegistro a ser deletado:")
            self.exibir_tabela_dados([registro])
            
            confirmacao = input("\n⚠️ Tem certeza que deseja deletar este registro? (s/n): ").strip().lower()
            
            if confirmacao == 's':
                if self.db.delete_sensor_data(record_id):
                    print("✅ Registro deletado com sucesso!")
                else:
                    print("❌ Erro ao deletar registro!")
            else:
                print("ℹ️ Operação cancelada.")
                
        except ValueError:
            print("❌ Digite um ID válido!")
        except Exception as e:
            print(f"❌ Erro ao deletar registro: {e}")
    
    def mostrar_estatisticas(self):
        """Exibe estatísticas detalhadas do sistema"""
        print("\n📈 ESTATÍSTICAS DO SISTEMA")
        print("-" * 25)
        
        try:
            stats = self.db.get_statistics()
            
            print(f"📊 Total de leituras: {stats['total_readings']}")
            print(f"💧 Umidade média: {stats['avg_humidity']}%")
            print(f"   • Mínima: {stats['min_humidity']}%")
            print(f"   • Máxima: {stats['max_humidity']}%")
            print(f"🧪 pH médio: {stats['avg_ph']}")
            print(f"   • Mínimo: {stats['min_ph']}")
            print(f"   • Máximo: {stats['max_ph']}")
            print(f"💦 Ativações da bomba: {stats['pump_activations']}")
            
            if stats['total_readings'] > 0:
                pct_irrigacao = (stats['pump_activations'] / stats['total_readings']) * 100
                print(f"📊 Percentual de irrigação: {pct_irrigacao:.1f}%")
                
        except Exception as e:
            print(f"❌ Erro ao calcular estatísticas: {e}")
    
    def buscar_por_periodo(self):
        """Busca registros por período específico"""
        print("\n🔍 BUSCAR POR PERÍODO")
        print("-" * 20)
        print("1. Últimas 24 horas")
        print("2. Última semana")
        print("3. Último mês")
        print("4. Período personalizado")
        
        opcao = input("Digite sua opção: ").strip()
        
        # Implementação simplificada - poderia ser expandida
        if opcao == "1":
            dados = self.db.get_sensor_data(50)  # Aproximadamente 24h com leituras a cada 30min
        elif opcao == "2":
            dados = self.db.get_sensor_data(336)  # 7 dias * 48 leituras/dia
        elif opcao == "3":
            dados = self.db.get_sensor_data(1440)  # 30 dias * 48 leituras/dia
        else:
            print("⚠️ Funcionalidade em desenvolvimento")
            return
        
        if dados:
            self.exibir_tabela_dados(dados)
            print(f"\n📊 Total de registros encontrados: {len(dados)}")
        else:
            print("📭 Nenhum registro encontrado para o período especificado!")
    
    def exportar_dados(self):
        """Exporta dados para arquivo JSON"""
        print("\n💾 EXPORTAR DADOS")
        print("-" * 15)
        
        try:
            dados = self.db.get_sensor_data(1000)
            
            if not dados:
                print("📭 Nenhum dado para exportar!")
                return
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"farmtech_export_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, default=str, ensure_ascii=False)
            
            print(f"✅ Dados exportados para: {filename}")
            print(f"📊 Total de registros exportados: {len(dados)}")
            
        except Exception as e:
            print(f"❌ Erro ao exportar dados: {e}")
    
    def buscar_por_id(self, record_id: int):
        """Busca um registro específico por ID"""
        dados = self.db.get_sensor_data(1000)
        for registro in dados:
            if registro['id'] == record_id:
                return registro
        return None
    
    def mostrar_registro(self, record_id: int):
        """Mostra um registro específico"""
        registro = self.buscar_por_id(record_id)
        if registro:
            self.exibir_tabela_dados([registro])
    
    def exibir_tabela_dados(self, dados):
        """Exibe dados em formato tabular"""
        if not dados:
            print("📭 Nenhum dado para exibir!")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<4} {'Data/Hora':<20} {'Umidade':<10} {'pH':<8} {'Fósforo':<10} {'Potássio':<10} {'Bomba':<8}")
        print("="*100)
        
        for registro in dados:
            fosforo = "✅ Sim" if registro['phosphorus'] else "❌ Não"
            potassio = "✅ Sim" if registro['potassium'] else "❌ Não"
            bomba = "🔴 ON" if registro['pump_status'] else "⚫ OFF"
            
            timestamp = registro['timestamp'][:19]  # Remove microsegundos
            
            print(f"{registro['id']:<4} {timestamp:<20} {registro['humidity']:<10.1f} {registro['ph_level']:<8.2f} {fosforo:<10} {potassio:<10} {bomba:<8}")
        
        print("="*100)

# Execução principal
if __name__ == "__main__":
    crud_system = FarmTechCRUD()
    crud_system.menu_principal()