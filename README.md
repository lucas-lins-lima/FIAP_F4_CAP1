# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto
FarmTech Solutions - Agricultura Digital

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/lucas-lins-lima/">Lucas Lins</a> 

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>


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

Link do documento completo: https://github.com/lucas-lins-lima/FIAP_F4_CAP1/blob/main/src/fase2/mer_documentation.md

### **FASE 3** ✅ - Sistema IoT com ESP32
- ✅ Simulação Wokwi

![Captura de tela 2025-06-19 212738](https://github.com/user-attachments/assets/d45f801d-e331-4718-bc21-03de060a751e)

- ✅ Sensores integrados
- ✅ Controle de irrigação
- ✅ Banco de dados com CRUD

Link do documento completo: https://github.com/lucas-lins-lima/FIAP_F4_CAP1/blob/main/document/fase3-hardware-system.md

### **FASE 4** ✅ - Machine Learning e Dashboard
- ✅ Integração Scikit-learn
- ✅ Dashboard Streamlit
- ✅ Otimizações ESP32

![Captura de tela 2025-06-19 224438](https://github.com/user-attachments/assets/2d4d22fe-8530-41e4-af2a-1605c85b9f0a)

- ✅ Sistema preditivo

Link do documento completo 1: https://github.com/lucas-lins-lima/FIAP_F4_CAP1/blob/main/document/fase4-ml-dashboard.md

Link do documento completo 2: https://github.com/lucas-lins-lima/FIAP_F4_CAP1/blob/main/src/fase4/esp32_optimized/memory_optimization.md

Link do video do Youtube: https://youtu.be/_vRdajyxBo8

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
├───backups
├───config
│       database.py
│       readme.md
│       settings.py
│
├───data
├───document
│   │   fase3-hardware-system.md
│   │   fase4-ml-dashboard.md
│   │
│   └───other
│           readme.md
│
├───logs
├───models
│       farmtech_irrigation_model.pkl
│
├───scripts
│   ├───database
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
    │   │   │   crud_operations.py
    │   │   │   database_manager.py
    │   │   │   data_analysis.py
    │   │   │   
    │   │   └───__pycache__
    │   │           database_manager.cpython-311.pyc
    │   │
    │   └───wokwi
    │           circuit.json
    │
    └───fase4
        │   train_ml_model.py
        │
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
        │   │   api_connections.py
        │   │   database_enhanced.py
        │   │
        │   └───__pycache__
        │           database_enhanced.cpython-311.pyc
        │
        ├───machine_learning
        │   │   data_preprocessing.py
        │   │   irrigation_predictor.py
        │   │   model_training.py
        │   │
        │   └───__pycache__
        │           data_preprocessing.cpython-311.pyc
        │           irrigation_predictor.cpython-311.pyc
        │           model_training.cpython-311.pyc
        │
        └───wokwi
                circuit_compatible.json
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
pip install numpy pandas scikit-learn joblib streamlit plotly matplotlib seaborn requests pytest black flake8 python-dotenv schedule

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
### Fase 4 - Machine Learning e Dashboard

1. Setup Automático 
```
cd farmtech-solutions
python scripts/deployment/setup.py
```
2. Configuração Manual
- Configurar .env
```
# FarmTech Solutions - Configurações de Ambiente

# Banco de Dados
DB_PATH=data/farmtech_production.db
DB_BACKUP_PATH=backups/
DB_RETENTION_DAYS=90

# Sensores
SENSOR_HUMIDITY_MIN=30.0
SENSOR_HUMIDITY_MAX=70.0
SENSOR_PH_MIN=6.0
SENSOR_PH_MAX=7.5
SENSOR_READING_INTERVAL=300

# API Externa (OpenWeatherMap)
OPENWEATHER_API_KEY=YOUR_API_KEY_HERE
OPENWEATHER_CITY=São Paulo
OPENWEATHER_COUNTRY=BR

# Machine Learning
ML_MODEL_PATH=models/farmtech_irrigation_model.pkl
ML_RETRAIN_DAYS=7
ML_CONFIDENCE_THRESHOLD=0.7

# Sistema
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
LOG_FILE=logs/farmtech.log
```
- Executar Dashboard
```
py -m streamlit run src/fase4/dashboard/streamlit_app.py
```
- Carregar código ESP32 manualmente:
  - Abrir src/fase4/esp32_optimized/main_optimized.cpp no Wokwi
  - Carregar src\fase4\wokwi\circuit_compatible.json
  - Execute a simulação

- Carregar código ESP32 Automatico:
  - Link: https://wokwi.com/projects/434240692467938305
  - Execute a simulação
  
## 🗃 Histórico de lançamentos

* 0.3.0 - 18/06/2025
    * Elaboração das fases 1 e 2
* 0.2.0 - 19/06/2025
    * Elaboração da fase 3
    * Conclussão da fase 1, 2 e 3
* 0.1.0 - 20/06/2025
    * Elaboração e conclusão da atividade 4

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


