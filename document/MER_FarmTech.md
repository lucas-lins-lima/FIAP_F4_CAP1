# MER - Modelo Entidade Relacionamento
## FarmTech Solutions - Sistema de Sensoriamento Agrícola

### 1. ENTIDADES E ATRIBUTOS

#### **FAZENDA**
- **id_fazenda** (PK) - INT - Identificador único da fazenda
- **nome_fazenda** - VARCHAR(100) - Nome da fazenda
- **proprietario** - VARCHAR(100) - Nome do proprietário
- **endereco** - VARCHAR(200) - Endereço completo
- **area_total** - DOUBLE - Área total da fazenda em m²
- **data_cadastro** - DATETIME - Data de cadastro no sistema

#### **CULTURA**
- **id_cultura** (PK) - INT - Identificador único da cultura
- **id_fazenda** (FK) - INT - Referência à fazenda
- **nome_plantacao** - VARCHAR(100) - Nome da plantação
- **tipo_cultura** - VARCHAR(50) - Tipo (Café, Milho, Soja)
- **area_plantada** - DOUBLE - Área plantada em m²
- **data_plantio** - DATE - Data do plantio
- **status_cultura** - VARCHAR(20) - Status (Ativa, Colhida, Preparando)
- **forma_geometrica** - VARCHAR(20) - Circular ou Retangular
- **dimensao_1** - DOUBLE - Raio ou Largura
- **dimensao_2** - DOUBLE - NULL ou Comprimento

#### **SENSOR**
- **id_sensor** (PK) - INT - Identificador único do sensor
- **id_cultura** (FK) - INT - Referência à cultura monitorada
- **tipo_sensor** - VARCHAR(20) - Tipo (umidade, pH, fosforo, potassio)
- **localizacao_x** - DOUBLE - Coordenada X do sensor
- **localizacao_y** - DOUBLE - Coordenada Y do sensor
- **status_sensor** - VARCHAR(20) - Status (Ativo, Inativo, Manutenção)
- **data_instalacao** - DATE - Data de instalação
- **modelo_sensor** - VARCHAR(50) - Modelo do equipamento

#### **LEITURA_SENSOR**
- **id_leitura** (PK) - INT - Identificador único da leitura
- **id_sensor** (FK) - INT - Referência ao sensor
- **valor_leitura** - DOUBLE - Valor coletado pelo sensor
- **unidade_medida** - VARCHAR(10) - Unidade (%, pH, ppm)
- **data_hora** - DATETIME - Momento da coleta
- **qualidade_sinal** - VARCHAR(20) - Qualidade do sinal (Excelente, Boa, Ruim)

#### **SISTEMA_IRRIGACAO**
- **id_irrigacao** (PK) - INT - Identificador único do sistema
- **id_cultura** (FK) - INT - Referência à cultura
- **tipo_sistema** - VARCHAR(30) - Tipo de irrigação (Gotejamento, Aspersão)
- **capacidade_vazao** - DOUBLE - Capacidade em L/min
- **status_sistema** - VARCHAR(20) - Status (Ativo, Inativo, Manutenção)

#### **ACIONAMENTO_IRRIGACAO**
- **id_acionamento** (PK) - INT - Identificador único do acionamento
- **id_irrigacao** (FK) - INT - Referência ao sistema de irrigação
- **data_hora_inicio** - DATETIME - Início da irrigação
- **data_hora_fim** - DATETIME - Fim da irrigação
- **quantidade_agua** - DOUBLE - Quantidade de água em litros
- **modo_acionamento** - VARCHAR(20) - Manual ou Automático
- **umidade_antes** - DOUBLE - Umidade antes da irrigação
- **umidade_depois** - DOUBLE - Umidade após a irrigação

#### **INSUMO**
- **id_insumo** (PK) - INT - Identificador único do insumo
- **nome_insumo** - VARCHAR(50) - Nome do insumo
- **tipo_insumo** - VARCHAR(30) - Tipo (Fertilizante, Defensivo, Corretivo)
- **composicao** - VARCHAR(100) - Composição química
- **unidade_aplicacao** - VARCHAR(10) - Unidade (L/m², kg/ha)
- **preco_unitario** - DOUBLE - Preço por unidade

#### **APLICACAO_INSUMO**
- **id_aplicacao** (PK) - INT - Identificador único da aplicação
- **id_cultura** (FK) - INT - Referência à cultura
- **id_insumo** (FK) - INT - Referência ao insumo
- **quantidade_aplicada** - DOUBLE - Quantidade aplicada
- **data_aplicacao** - DATE - Data da aplicação
- **responsavel** - VARCHAR(100) - Responsável pela aplicação
- **observacoes** - TEXT - Observações sobre a aplicação

### 2. RELACIONAMENTOS E CARDINALIDADES

#### **FAZENDA → CULTURA (1:N)**
- Uma fazenda pode ter várias culturas
- Uma cultura pertence a apenas uma fazenda

#### **CULTURA → SENSOR (1:N)**
- Uma cultura pode ter vários sensores
- Um sensor monitora apenas uma cultura

#### **SENSOR → LEITURA_SENSOR (1:N)**
- Um sensor pode ter várias leituras
- Uma leitura pertence a apenas um sensor

#### **CULTURA → SISTEMA_IRRIGACAO (1:N)**
- Uma cultura pode ter vários sistemas de irrigação
- Um sistema de irrigação atende apenas uma cultura

#### **SISTEMA_IRRIGACAO → ACIONAMENTO_IRRIGACAO (1:N)**
- Um sistema pode ter vários acionamentos
- Um acionamento pertence a apenas um sistema

#### **CULTURA → APLICACAO_INSUMO (1:N)**
- Uma cultura pode ter várias aplicações de insumo
- Uma aplicação é feita em apenas uma cultura

#### **INSUMO → APLICACAO_INSUMO (1:N)**
- Um insumo pode ser aplicado várias vezes
- Uma aplicação usa apenas um tipo de insumo

### 3. REGRAS DE NEGÓCIO

1. **Sensor deve estar ativo** para gerar leituras válidas
2. **Irrigação automática** só pode ser acionada com base em leituras de sensores de umidade
3. **Aplicação de insumos** deve respeitar intervalos mínimos entre aplicações
4. **Uma cultura** só pode ser cadastrada em fazendas ativas
5. **Leituras de sensores** devem ter timestamps únicos por sensor
6. **Sistema de irrigação** deve ter vazão compatível com a área da cultura

### 4. ÍNDICES RECOMENDADOS

- **idx_leitura_sensor_data** - Para consultas por período
- **idx_cultura_tipo** - Para filtros por tipo de cultura
- **idx_sensor_status** - Para monitoramento de sensores ativos
- **idx_irrigacao_data** - Para relatórios de consumo de água
