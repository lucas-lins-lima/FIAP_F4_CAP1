# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto
FarmTech Solutions - Agricultura Digital

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 1</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 2</a>
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 3</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 4</a> 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do integrante 5</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Tutor</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

A **FarmTech Solutions** é uma startup inovadora focada em soluções tecnológicas para agricultura digital. Este projeto desenvolve um sistema completo de monitoramento e gestão agrícola, evoluindo através de 4 fases distintas.

## 🎯 Objetivos por Fase

### **FASE 1** ✅ - Sistema de Cálculos Agrícolas
- ✅ Aplicação Python para 4 tipos de culturas
- ✅ Cálculo de áreas geométricas específicas
- ✅ Gestão de insumos e manejo
- ✅ Sistema de menu interativo
- ✅ Análise estatística em R

### **FASE 2** ✅ - Modelagem de Banco de Dados
- ✅ Modelagem MER/DER
- ✅ Sistema de sensores (pH, umidade, NPK)
- ✅ SQL Developer Data Modeler

### **FASE 3** ✅ - Sistema IoT com ESP32
- ✅ Simulação Wokwi
- ✅ Sensores integrados
- ✅ Controle de irrigação
- ✅ Banco de dados com CRUD

## 🔧 Componentes do Sistema (Fase 3)

### Hardware Simulado (Wokwi)
- **ESP32**: Microcontrolador principal
- **DHT22**: Sensor de umidade do solo
- **LDR**: Sensor de pH (simulado)
- **Botões**: Sensores de fósforo e potássio
- **Relé**: Controle da bomba de irrigação
- **LED**: Indicador de status do sistema

![Captura de tela 2025-06-19 212738](https://github.com/user-attachments/assets/d45f801d-e331-4718-bc21-03de060a751e)

### Software
- **C/C++**: Código do microcontrolador
- **Python**: Banco de dados e análise
- **SQLite**: Armazenamento local de dados

### **FASE 4** ✅ - Machine Learning e Dashboard
- ✅ Integração Scikit-learn
- ✅ Dashboard Streamlit
- ✅ Otimizações ESP32
- ✅ Sistema preditivo

## 🌱 Culturas Suportadas

| Cultura | Geometria | Insumo Principal | Dosagem |
|---------|-----------|------------------|---------|
| 🌿 **Soja** | Retangular | Glifosato | 3L/hectare |
| 🌽 **Milho** | Circular (Pivô) | Ureia | 200kg/hectare |
| ☕ **Café** | Trapezoidal | Fosfato | 150kg/hectare |
| 🎋 **Cana-de-açúcar** | Triangular | NPK Líquido | 500mL/metro |

## 📁 Estrutura do Projeto
```
│   .gitattributes
│   .gitignore
│   README.md
│   
├───.github
│   └───workflows
│           ci.yml
│
├───assets
│   │   logo-fiap.png
│   │
│   ├───diagrams
│   └───images
│       ├───dashboard-screenshots
│       ├───serial-plotter
│       └───system-demo
├───config
│       database.py
│       readme.md
│       settings.py
│
├───document
│   │   fase1-requirements.md
│   │   fase2-database-design.md
│   │   fase3-hardware-system.md
│   │   fase4-ml-dashboard.md
│   │
│   └───other
│           readme.md
│
├───scripts
│   ├───database
│   │       backup_scripts.py
│   │       create_tables.sql
│   │       seed_data.sql
│   │
│   └───deployment
│           requirements.txt
│           setup.py
│
└───src
    ├───fase1
    │   │   agriculture_calculator.py
    │   │   analysis.R
    │   │   data_for_r.csv
    │   │   data_manager.py
    │   │   farmtech_data.json
    │   │   main.py
    │   │
    │   └───__pycache__
    │           agriculture_calculator.cpython-311.pyc
    │           data_manager.cpython-311.pyc
    │
    ├───fase2
    │       database_schema.sql
    │       farmtech_model.dmd
    │       mer_documentation.md
    │
    ├───fase3
    │   ├───esp32
    │   │       main.cpp
    │   │       platformio.ini
    │   │       sensors.h
    │   │
    │   ├───python
    │   │       crud_operations.py
    │   │       database_manager.py
    │   │       data_analysis.py
    │   │
    │   └───wokwi
    │           circuit.json
    │
    └───fase4
        ├───dashboard
        │   │   streamlit_app.py
        │   │
        │   ├───components
        │   └───static
        ├───esp32_optimized
        │       lcd_display.h
        │       main_optimized.cpp
        │       memory_optimization.md
        │
        ├───integration
        │       api_connections.py
        │       database_enhanced.py
        │
        └───machine_learning
                data_preprocessing.py
                irrigation_predictor.py
                model_training.py
```
## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

### **Pré-requisitos**
```
bash
# Python 3.8+
pip install -r scripts/deployment/requirements.txt
```
# Bibliotecas específicas
pip install sqlite3 pandas matplotlib seaborn pyserial numpy

### Fase 1 - Sistema Python
```
bash
cd src/fase1
python main.py
```
### Fase 1 - Sistema R
```
cd src/fase1
Rscript analysis.R
```
### Fase 2 - Banco de Dados
```
cd src/fase2
# Executar scripts SQL no MySQL/SQLite
sqlite3 farmtech.db < database_schema.sql
```
### Fase 3 - Sistema IoT

1.Simulação no Wokwi (manualmente):
- Abra o arquivo src/fase3/wokwi/circuit.json no Wokwi
- Carregue o código src/fase3/esp32/main.cpp
- Execute a simulação

2. Simulação no Wokwi (automatico)
- link: https://wokwi.com/projects/434236257248040961
- Execute a simulação

3. Sistema CRUD
```
cd src/fase3/python
python crud_operations.py
```
4. Análise de Dados
```
python data_analysis.py
```
### Fase 4 - 

## 🗃 Histórico de lançamentos

* 0.5.0 - XX/XX/2024
    * 
* 0.4.0 - XX/XX/2024
    * 
* 0.3.0 - XX/XX/2024
    * 
* 0.2.0 - XX/XX/2024
    * 
* 0.1.0 - XX/XX/2024
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


