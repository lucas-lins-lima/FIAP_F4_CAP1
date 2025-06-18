-- =====================================================
-- FarmTech Solutions - Criação do Banco de Dados
-- Fase 2: Estrutura Completa do Sistema de Sensoriamento
-- =====================================================

-- Criar banco de dados
CREATE DATABASE farmtech_solutions;
USE farmtech_solutions;

-- =====================================================
-- TABELA: FAZENDA
-- =====================================================
CREATE TABLE fazenda (
    id_fazenda INT PRIMARY KEY AUTO_INCREMENT,
    nome_fazenda VARCHAR(100) NOT NULL,
    proprietario VARCHAR(100) NOT NULL,
    endereco VARCHAR(200),
    area_total DOUBLE NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_fazenda VARCHAR(20) DEFAULT 'Ativa',
    
    INDEX idx_fazenda_proprietario (proprietario),
    INDEX idx_fazenda_status (status_fazenda)
);

-- =====================================================
-- TABELA: CULTURA
-- =====================================================
CREATE TABLE cultura (
    id_cultura INT PRIMARY KEY AUTO_INCREMENT,
    id_fazenda INT NOT NULL,
    nome_plantacao VARCHAR(100) NOT NULL,
    tipo_cultura VARCHAR(50) NOT NULL,
    area_plantada DOUBLE NOT NULL,
    data_plantio DATE NOT NULL,
    status_cultura VARCHAR(20) DEFAULT 'Ativa',
    forma_geometrica VARCHAR(20) NOT NULL,
    dimensao_1 DOUBLE NOT NULL,
    dimensao_2 DOUBLE NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_fazenda) REFERENCES fazenda(id_fazenda),
    INDEX idx_cultura_tipo (tipo_cultura),
    INDEX idx_cultura_status (status_cultura),
    INDEX idx_cultura_data_plantio (data_plantio)
);

-- =====================================================
-- TABELA: SENSOR
-- =====================================================
CREATE TABLE sensor (
    id_sensor INT PRIMARY KEY AUTO_INCREMENT,
    id_cultura INT NOT NULL,
    tipo_sensor VARCHAR(20) NOT NULL,
    localizacao_x DOUBLE,
    localizacao_y DOUBLE,
    status_sensor VARCHAR(20) DEFAULT 'Ativo',
    data_instalacao DATE NOT NULL,
    modelo_sensor VARCHAR(50),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_cultura) REFERENCES cultura(id_cultura),
    INDEX idx_sensor_tipo (tipo_sensor),
    INDEX idx_sensor_status (status_sensor),
    INDEX idx_sensor_cultura (id_cultura)
);

-- =====================================================
-- TABELA: LEITURA_SENSOR
-- =====================================================
CREATE TABLE leitura_sensor (
    id_leitura INT PRIMARY KEY AUTO_INCREMENT,
    id_sensor INT NOT NULL,
    valor_leitura DOUBLE NOT NULL,
    unidade_medida VARCHAR(10) NOT NULL,
    data_hora DATETIME NOT NULL,
    qualidade_sinal VARCHAR(20) DEFAULT 'Boa',
    
    FOREIGN KEY (id_sensor) REFERENCES sensor(id_sensor),
    INDEX idx_leitura_data_hora (data_hora),
    INDEX idx_leitura_sensor (id_sensor),
    UNIQUE KEY uk_sensor_data_hora (id_sensor, data_hora)
);

-- =====================================================
-- TABELA: SISTEMA_IRRIGACAO
-- =====================================================
CREATE TABLE sistema_irrigacao (
    id_irrigacao INT PRIMARY KEY AUTO_INCREMENT,
    id_cultura INT NOT NULL,
    tipo_sistema VARCHAR(30) NOT NULL,
    capacidade_vazao DOUBLE NOT NULL,
    status_sistema VARCHAR(20) DEFAULT 'Ativo',
    data_instalacao DATE NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_cultura) REFERENCES cultura(id_cultura),
    INDEX idx_irrigacao_cultura (id_cultura),
    INDEX idx_irrigacao_status (status_sistema)
);

-- =====================================================
-- TABELA: ACIONAMENTO_IRRIGACAO
-- =====================================================
CREATE TABLE acionamento_irrigacao (
    id_acionamento INT PRIMARY KEY AUTO_INCREMENT,
    id_irrigacao INT NOT NULL,
    data_hora_inicio DATETIME NOT NULL,
    data_hora_fim DATETIME,
    quantidade_agua DOUBLE,
    modo_acionamento VARCHAR(20) NOT NULL,
    umidade_antes DOUBLE,
    umidade_depois DOUBLE,
    observacoes TEXT,
    
    FOREIGN KEY (id_irrigacao) REFERENCES sistema_irrigacao(id_irrigacao),
    INDEX idx_acionamento_data (data_hora_inicio),
    INDEX idx_acionamento_irrigacao (id_irrigacao)
);

-- =====================================================
-- TABELA: INSUMO
-- =====================================================
CREATE TABLE insumo (
    id_insumo INT PRIMARY KEY AUTO_INCREMENT,
    nome_insumo VARCHAR(50) NOT NULL,
    tipo_insumo VARCHAR(30) NOT NULL,
    composicao VARCHAR(100),
    unidade_aplicacao VARCHAR(10) NOT NULL,
    preco_unitario DOUBLE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_insumo_tipo (tipo_insumo),
    INDEX idx_insumo_nome (nome_insumo)
);

-- =====================================================
-- TABELA: APLICACAO_INSUMO
-- =====================================================
CREATE TABLE aplicacao_insumo (
    id_aplicacao INT PRIMARY KEY AUTO_INCREMENT,
    id_cultura INT NOT NULL,
    id_insumo INT NOT NULL,
    quantidade_aplicada DOUBLE NOT NULL,
    data_aplicacao DATE NOT NULL,
    responsavel VARCHAR(100),
    observacoes TEXT,
    custo_total DOUBLE,
    
    FOREIGN KEY (id_cultura) REFERENCES cultura(id_cultura),
    FOREIGN KEY (id_insumo) REFERENCES insumo(id_insumo),
    INDEX idx_aplicacao_data (data_aplicacao),
    INDEX idx_aplicacao_cultura (id_cultura),
    INDEX idx_aplicacao_insumo (id_insumo)
);

-- =====================================================
-- INSERÇÃO DE DADOS DE EXEMPLO
-- =====================================================

-- Inserir fazendas
INSERT INTO fazenda (nome_fazenda, proprietario, endereco, area_total) VALUES
('Fazenda Santa Maria', 'João Silva', 'Zona Rural, Ribeirão Preto - SP', 50000),
('Sítio Boa Vista', 'Maria Santos', 'Estrada do Campo, Franca - SP', 25000),
('Fazenda Esperança', 'Pedro Oliveira', 'Rod. BR-050, Uberaba - MG', 75000);

-- Inserir culturas
INSERT INTO cultura (id_fazenda, nome_plantacao, tipo_cultura, area_plantada, data_plantio, forma_geometrica, dimensao_1, dimensao_2) VALUES
(1, 'Cafezal Norte', 'Café', 1963.5, '2024-03-15', 'Circular', 25.0, NULL),
(1, 'Plantio Milho A', 'Milho', 5000.0, '2024-04-01', 'Retangular', 100.0, 50.0),
(2, 'Sojal Sul', 'Soja', 4800.0, '2024-03-20', 'Retangular', 80.0, 60.0),
(3, 'Cafezal Central', 'Café', 2827.4, '2024-02-10', 'Circular', 30.0, NULL),
(3, 'Campo de Milho', 'Milho', 4800.0, '2024-04-15', 'Retangular', 120.0, 40.0);

-- Inserir sensores
INSERT INTO sensor (id_cultura, tipo_sensor, localizacao_x, localizacao_y, data_instalacao, modelo_sensor) VALUES
(1, 'umidade', 12.5, 12.5, '2024-03-16', 'DHT22'),
(1, 'pH', 18.0, 8.0, '2024-03-16', 'PH-4502C'),
(1, 'fosforo', 20.0, 15.0, '2024-03-16', 'NPK-Sensor-P'),
(1, 'potassio', 22.0, 18.0, '2024-03-16', 'NPK-Sensor-K'),
(2, 'umidade', 50.0, 25.0, '2024-04-02', 'DHT22'),
(2, 'pH', 75.0, 30.0, '2024-04-02', 'PH-4502C'),
(3, 'umidade', 40.0, 30.0, '2024-03-21', 'DHT22'),
(3, 'fosforo', 45.0, 35.0, '2024-03-21', 'NPK-Sensor-P'),
(3, 'potassio', 50.0, 40.0, '2024-03-21', 'NPK-Sensor-K');

-- Inserir sistemas de irrigação
INSERT INTO sistema_irrigacao (id_cultura, tipo_sistema, capacidade_vazao, data_instalacao) VALUES
(1, 'Gotejamento', 150.0, '2024-03-17'),
(2, 'Aspersão', 300.0, '2024-04-03'),
(3, 'Gotejamento', 200.0, '2024-03-22'),
(4, 'Aspersão', 180.0, '2024-02-12'),
(5, 'Aspersão', 350.0, '2024-04-16');

-- Inserir insumos
INSERT INTO insumo (nome_insumo, tipo_insumo, composicao, unidade_aplicacao, preco_unitario) VALUES
('Fosfato Monoamônico', 'Fertilizante', 'NH4H2PO4', 'L/m²', 15.50),
('NPK 10-10-10', 'Fertilizante', '10% N, 10% P2O5, 10% K2O', 'L/m²', 12.30),
('Cloreto de Potássio', 'Fertilizante', 'KCl 60%', 'L/m²', 18.90),
('Calcário Dolomítico', 'Corretivo', 'CaMg(CO3)2', 'kg/ha', 0.25),
('Herbicida Glifosato', 'Defensivo', 'C3H8NO5P 48%', 'L/ha', 35.00);

-- =====================================================
-- VIEWS PARA RELATÓRIOS
-- =====================================================

-- View: Resumo por fazenda
CREATE VIEW vw_resumo_fazenda AS
SELECT 
    f.nome_fazenda,
    f.proprietario,
    COUNT(c.id_cultura) as total_culturas,
    SUM(c.area_plantada) as area_total_plantada,
    f.area_total,
    ROUND((SUM(c.area_plantada) / f.area_total) * 100, 2) as percentual_utilizado
FROM fazenda f
LEFT JOIN cultura c ON f.id_fazenda = c.id_fazenda
GROUP BY f.id_fazenda;

-- View: Monitoramento de sensores
CREATE VIEW vw_status_sensores AS
SELECT 
    f.nome_fazenda,
    c.nome_plantacao,
    c.tipo_cultura,
    s.tipo_sensor,
    s.status_sensor,
    COUNT(l.id_leitura) as total_leituras,
    MAX(l.data_hora) as ultima_leitura
FROM fazenda f
JOIN cultura c ON f.id_fazenda = c.id_fazenda
JOIN sensor s ON c.id_cultura = s.id_cultura
LEFT JOIN leitura_sensor l ON s.id_sensor = l.id_sensor
GROUP BY f.id_fazenda, c.id_cultura, s.id_sensor;

-- =====================================================
-- PROCEDURES PARA OPERAÇÕES COMUNS
-- =====================================================

DELIMITER //

-- Procedure: Inserir leitura de sensor
CREATE PROCEDURE sp_inserir_leitura(
    IN p_id_sensor INT,
    IN p_valor DOUBLE,
    IN p_unidade VARCHAR(10)
)
BEGIN
    INSERT INTO leitura_sensor (id_sensor, valor_leitura, unidade_medida, data_hora)
    VALUES (p_id_sensor, p_valor, p_unidade, NOW());
END //

-- Procedure: Acionar irrigação
CREATE PROCEDURE sp_acionar_irrigacao(
    IN p_id_irrigacao INT,
    IN p_modo VARCHAR(20),
    IN p_umidade_antes DOUBLE
)
BEGIN
    INSERT INTO acionamento_irrigacao (id_irrigacao, data_hora_inicio, modo_acionamento, umidade_antes)
    VALUES (p_id_irrigacao, NOW(), p_modo, p_umidade_antes);
END //

DELIMITER ;

-- =====================================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- =====================================================

CREATE INDEX idx_leitura_valor ON leitura_sensor(valor_leitura);
CREATE INDEX idx_acionamento_modo ON acionamento_irrigacao(modo_acionamento);
CREATE INDEX idx_aplicacao_custo ON aplicacao_insumo(custo_total);

-- =====================================================
-- COMENTÁRIOS NAS TABELAS
-- =====================================================

ALTER TABLE fazenda COMMENT = 'Cadastro das fazendas do sistema';
ALTER TABLE cultura COMMENT = 'Culturas plantadas em cada fazenda';
ALTER TABLE sensor COMMENT = 'Sensores instalados para monitoramento';
ALTER TABLE leitura_sensor COMMENT = 'Dados coletados pelos sensores';
ALTER TABLE sistema_irrigacao COMMENT = 'Sistemas de irrigação instalados';
ALTER TABLE acionamento_irrigacao COMMENT = 'Histórico de acionamentos de irrigação';
ALTER TABLE insumo COMMENT = 'Cadastro de insumos disponíveis';
ALTER TABLE aplicacao_insumo COMMENT = 'Histórico de aplicações de insumos';
