# Documentação da Fase 2 - Modelagem de Banco de Dados
## FarmTech Solutions

### 📋 Resumo Executivo

A Fase 2 do projeto FarmTech Solutions consistiu na modelagem completa do banco de dados para suportar o sistema de sensoriamento agrícola inteligente. O modelo contempla desde o cadastro básico de fazendas até o controle detalhado de sensores, irrigação e aplicação de insumos.

### 🎯 Objetivos Alcançados

✅ **Identificação completa das entidades** e seus atributos  
✅ **Definição de relacionamentos** com cardinalidades corretas  
✅ **Especificação de tipos de dados** apropriados  
✅ **Criação do DER visual** no SQL Developer Data Modeler  
✅ **Implementação de scripts SQL** funcionais  
✅ **Desenvolvimento de consultas** para relatórios  

### 🗄️ Estrutura do Banco de Dados

#### Entidades Principais:
- **FAZENDA** - Cadastro das propriedades rurais
- **CULTURA** - Plantações e suas características
- **SENSOR** - Dispositivos de monitoramento
- **LEITURA_SENSOR** - Dados coletados em tempo real
- **SISTEMA_IRRIGACAO** - Infraestrutura de irrigação
- **ACIONAMENTO_IRRIGACAO** - Histórico de irrigações
- **INSUMO** - Produtos agrícolas utilizados
- **APLICACAO_INSUMO** - Controle de aplicações

#### Relacionamentos Implementados:
- **1:N** - Fazenda → Cultura
- **1:N** - Cultura → Sensor
- **1:N** - Sensor → Leitura
- **1:N** - Cultura → Sistema Irrigação
- **1:N** - Sistema Irrigação → Acionamento
- **N:N** - Cultura ↔ Insumo (através de Aplicação)

### 📊 Funcionalidades Suportadas

#### Monitoramento em Tempo Real:
- Coleta automática de dados de sensores
- Histórico completo de leituras
- Alertas para valores críticos
- Status de funcionamento dos sensores

#### Controle de Irrigação:
- Acionamento manual e automático
- Cálculo de consumo de água
- Eficiência da irrigação
- Relatórios de uso por período

#### Gestão de Insumos:
- Controle de estoque e custos
- Histórico de aplicações
- Análise de produtividade
- Planejamento de compras

### 🔍 Consultas Implementadas

#### Relatórios de Monitoramento:
```sql
-- Exemplo: Umidade dos últimos 7 dias
SELECT f.nome_fazenda, c.nome_plantacao, l.valor_leitura, l.data_hora
FROM leitura_sensor l
JOIN sensor s ON l.id_sensor = s.id_sensor
JOIN cultura c ON s.id_cultura = c.id_cultura
JOIN fazenda f ON c.id_fazenda = f.id_fazenda
WHERE s.tipo_sensor = 'umidade' 
  AND l.data_hora >= DATE_SUB(NOW(), INTERVAL 7 DAY);
