# Fase 3: Sistema de Sensores Físicos

## 🔧 Componentes do Sistema (Fase 3)

### Hardware Simulado (Wokwi)
- **ESP32**: Microcontrolador principal
- **DHT22**: Sensor de umidade do solo
- **LDR**: Sensor de pH (simulado)
- **Botões**: Sensores de fósforo e potássio
- **Relé**: Controle da bomba de irrigação
- **LED**: Indicador de status do sistema

### Software
- **C/C++**: Código do microcontrolador
- **Python**: Banco de dados e análise
- **SQLite**: Armazenamento local de dados

## 📊 Funcionalidades

### Sistema de Sensores
- ✅ Monitoramento de umidade do solo
- ✅ Medição de pH
- ✅ Detecção de nutrientes (P e K)
- ✅ Controle automatizado de irrigação
- ✅ Logging de dados em tempo real

### Banco de Dados
- ✅ Operações CRUD completas
- ✅ Armazenamento histórico
- ✅ Consultas por período
- ✅ Exportação de dados
- ✅ Estatísticas automatizadas

### Análise de Dados
- ✅ Tendências de umidade
- ✅ Análise de pH
- ✅ Disponibilidade de nutrientes
- ✅ Eficiência da irrigação
- ✅ Relatórios completos

## 🎛️ Lógica de Controle da Irrigação

O sistema ativa a bomba de irrigação quando:

- Umidade do solo < 30%
- pH fora da faixa ideal (6.0 - 7.5)
- Ausência de fósforo ou potássio
- Combinação de condições adversas

## 📈 Análise e Monitoramento

**Dados Coletados**
- Timestamp da leitura
- Umidade do solo (%)
- Nível de pH (0-14)
- Presença de fósforo (boolean)
- Presença de potássio (boolean)
- Status da bomba (ligada/desligada)

**Métricas Calculadas**
- Médias e desvios padrão
- Frequência de irrigação
- Eficiência do sistema
- Classificação das condições

## 🛠️ Tecnologias Utilizadas

- Hardware: ESP32, Sensores diversos
- Linguagens: C/C++, Python
- Banco de Dados: SQLite
- Análise: NumPy, Pandas, Matplotlib
- Simulação: Wokwi.com
- Versionamento: Git/GitHub