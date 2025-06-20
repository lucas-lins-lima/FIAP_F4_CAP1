-- ===============================================
-- FarmTech Solutions - Sistema de Sensoriamento Agrícola
-- Script de Criação do Banco de Dados
-- Fase 2: Modelagem de Dados
-- Data: Dezembro 2024
-- ===============================================

-- Configurações iniciais
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

-- ===============================================
-- CRIAÇÃO DO SCHEMA
-- ===============================================
CREATE SCHEMA IF NOT EXISTS `farmtech_solutions` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `farmtech_solutions`;

-- ===============================================
-- TABELA: PROPRIEDADES
-- ===============================================
CREATE TABLE IF NOT EXISTS `PROPRIEDADES` (
    `id_propriedade` INT NOT NULL AUTO_INCREMENT,
    `nome_propriedade` VARCHAR(100) NOT NULL,
    `endereco` VARCHAR(200) NOT NULL,
    `cidade` VARCHAR(50) NOT NULL,
    `estado` CHAR(2) NOT NULL,
    `cep` VARCHAR(10) NOT NULL,
    `area_total` DECIMAL(10,2) NOT NULL,
    `latitude` DECIMAL(10,8) NULL,
    `longitude` DECIMAL(11,8) NULL,
    `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ativo` BOOLEAN NOT NULL DEFAULT TRUE,
    
    PRIMARY KEY (`id_propriedade`),
    
    -- Constraints
    CONSTRAINT `chk_area_total` CHECK (`area_total` > 0),
    CONSTRAINT `chk_estado` CHECK (`estado` REGEXP '^[A-Z]{2}$'),
    CONSTRAINT `chk_cep` CHECK (`cep` REGEXP '^[0-9]{5}-?[0-9]{3}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Propriedades rurais cadastradas no sistema';

-- ===============================================
-- TABELA: USUARIOS
-- ===============================================
CREATE TABLE IF NOT EXISTS `USUARIOS` (
    `id_usuario` INT NOT NULL AUTO_INCREMENT,
    `nome_completo` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `telefone` VARCHAR(20) NULL,
    `tipo_usuario` ENUM('PROPRIETARIO', 'TECNICO', 'ADMINISTRADOR') NOT NULL,
    `data_nascimento` DATE NULL,
    `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ultimo_acesso` DATETIME NULL,
    `ativo` BOOLEAN NOT NULL DEFAULT TRUE,
    
    PRIMARY KEY (`id_usuario`),
    UNIQUE INDEX `email_UNIQUE` (`email` ASC),
    
    -- Constraints
    CONSTRAINT `chk_email` CHECK (`email` REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Usuários do sistema (produtores e técnicos)';

-- ===============================================
-- TABELA: CULTURAS
-- ===============================================
CREATE TABLE IF NOT EXISTS `CULTURAS` (
    `id_cultura` INT NOT NULL AUTO_INCREMENT,
    `nome_cultura` VARCHAR(50) NOT NULL,
    `nome_cientifico` VARCHAR(100) NULL,
    `ph_ideal_min` DECIMAL(3,1) NOT NULL,
    `ph_ideal_max` DECIMAL(3,1) NOT NULL,
    `umidade_ideal_min` DECIMAL(5,2) NOT NULL,
    `umidade_ideal_max` DECIMAL(5,2) NOT NULL,
    `fosforo_ideal` DECIMAL(6,2) NOT NULL,
    `potassio_ideal` DECIMAL(6,2) NOT NULL,
    `ciclo_dias` INT NOT NULL,
    `descricao` TEXT NULL,
    `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`id_cultura`),
    UNIQUE INDEX `nome_cultura_UNIQUE` (`nome_cultura` ASC),
    
    -- Constraints
    CONSTRAINT `chk_ph_range` CHECK (`ph_ideal_min` >= 0 AND `ph_ideal_max` <= 14 AND `ph_ideal_min` < `ph_ideal_max`),
    CONSTRAINT `chk_umidade_range` CHECK (`umidade_ideal_min` >= 0 AND `umidade_ideal_max` <= 100 AND `umidade_ideal_min` < `umidade_ideal_max`),
    CONSTRAINT `chk_nutrientes` CHECK (`fosforo_ideal` >= 0 AND `potassio_ideal` >= 0),
    CONSTRAINT `chk_ciclo` CHECK (`ciclo_dias` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Tipos de culturas suportadas pelo sistema';

-- ===============================================
-- TABELA: AREAS_PLANTIO
-- ===============================================
CREATE TABLE IF NOT EXISTS `AREAS_PLANTIO` (
    `id_area` INT NOT NULL AUTO_INCREMENT,
    `id_propriedade` INT NOT NULL,
    `id_cultura` INT NOT NULL,
    `id_usuario_responsavel` INT NOT NULL,
    `nome_area` VARCHAR(100) NOT NULL,
    `geometria` ENUM('RETANGULAR', 'CIRCULAR', 'TRAPEZOIDAL', 'TRIANGULAR') NOT NULL,
    `area_hectares` DECIMAL(10,4) NOT NULL,
    `coordenadas_json` JSON NULL,
    `data_plantio` DATE NOT NULL,
    `data_previsao_colheita` DATE NOT NULL,
    `status` ENUM('ATIVO', 'INATIVO', 'COLHIDO') NOT NULL DEFAULT 'ATIVO',
    `observacoes` TEXT NULL,
    `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`id_area`),
    INDEX `fk_areas_propriedades_idx` (`id_propriedade` ASC),
    INDEX `fk_areas_culturas_idx` (`id_cultura` ASC),
    INDEX `fk_areas_usuarios_idx` (`id_usuario_responsavel` ASC),
    INDEX `idx_status_data` (`status` ASC, `data_plantio` ASC),
    
    -- Constraints
    CONSTRAINT `chk_area_hectares` CHECK (`area_hectares` > 0),
    CONSTRAINT `chk_datas_plantio` CHECK (`data_previsao_colheita` > `data_plantio`),
    
    -- Foreign Keys
    CONSTRAINT `fk_areas_propriedades`
        FOREIGN KEY (`id_propriedade`)
        REFERENCES `PROPRIEDADES` (`id_propriedade`)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_areas_culturas`
        FOREIGN KEY (`id_cultura`)
        REFERENCES `CULTURAS` (`id_cultura`)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_areas_usuarios`
        FOREIGN KEY (`id_usuario_responsavel`)
        REFERENCES `USUARIOS` (`id_usuario`)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Áreas específicas de plantio dentro das propriedades';

-- ===============================================
-- TABELA: SENSORES
-- ===============================================
CREATE TABLE IF NOT EXISTS `SENSORES` (
    `id_sensor` INT NOT NULL AUTO_INCREMENT,
    `id_area` INT NOT NULL,
    `tipo_sensor` ENUM('UMIDADE', 'PH', 'FOSFORO', 'POTASSIO') NOT NULL,
    `modelo` VARCHAR(50) NOT NULL,
    `numero_serie` VARCHAR(50) NULL,
    `localizacao_x` DECIMAL(8,4) NULL,
    `localizacao_y` DECIMAL(8,4) NULL,
    `profundidade_cm` INT NULL,
    `data_instalacao` DATE NOT NULL,
    `data_ultima_manutencao` DATE NULL,
    `intervalo_leitura_min` INT NOT NULL DEFAULT 15,
    `status` ENUM('ATIVO', 'INATIVO', 'MANUTENCAO') NOT NULL DEFAULT 'ATIVO',
    `data_cadastro` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`id_sensor`),
    UNIQUE INDEX `numero_serie_UNIQUE` (`numero_serie` ASC),
    INDEX `fk_sensores_areas_idx` (`id_area` ASC),
    INDEX `idx_tipo_status` (`tipo_sensor` ASC, `status` ASC),
    
    -- Constraints
    CONSTRAINT `chk_intervalo_leitura` CHECK (`intervalo_leitura_min` > 0),
    CONSTRAINT `chk_profundidade` CHECK (`profundidade_cm` >= 0),
    
    -- Foreign Keys
    CONSTRAINT `fk_sensores_areas`
        FOREIGN KEY (`id_area`)
        REFERENCES `AREAS_PLANTIO` (`id_area`)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Sensores instalados nas áreas de plantio';

-- ===============================================
-- TABELA: LEITURAS_SENSORES
-- ===============================================
CREATE TABLE IF NOT EXISTS `LEITURAS_SENSORES` (
    `id_leitura` BIGINT NOT NULL AUTO_INCREMENT,
    `id_sensor` INT NOT NULL,
    `valor` DECIMAL(10,4) NOT NULL,
    `unidade` VARCHAR(10) NOT NULL,
    `data_hora_leitura` DATETIME NOT NULL,
    `qualidade_sinal` INT NULL DEFAULT 100,
    `temperatura_ambiente` DECIMAL(5,2) NULL,
    `observacoes` VARCHAR(255) NULL,
    `processado` BOOLEAN NOT NULL DEFAULT FALSE,
    
    PRIMARY KEY (`id_leitura`),
    INDEX `fk_leituras_sensores_idx` (`id_sensor` ASC),
    INDEX `idx_sensor_data` (`id_sensor` ASC, `data_hora_leitura` ASC),
    INDEX `idx_data_hora` (`data_hora_leitura` ASC),
    INDEX `idx_processado` (`processado` ASC),
    
    -- Constraints
    CONSTRAINT `chk_qualidade_sinal` CHECK (`qualidade_sinal` >= 0 AND `qualidade_sinal` <= 100),
    
    -- Foreign Keys
    CONSTRAINT `fk_leituras_sensores`
        FOREIGN KEY (`id_sensor`)
        REFERENCES `SENSORES` (`id_sensor`)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Dados coletados pelos sensores em tempo real';

-- Particionamento por data para otimizar consultas históricas
-- ALTER TABLE LEITURAS_SENSORES PARTITION BY RANGE (YEAR(data_hora_leitura)) (
--     PARTITION p2023 VALUES LESS THAN (2024),
--     PARTITION p2024 VALUES LESS THAN (2025),
--     PARTITION p2025 VALUES LESS THAN (2026),
--     PARTITION p_future VALUES LESS THAN MAXVALUE
-- );

-- ===============================================
-- TABELA: IRRIGACOES
-- ===============================================
CREATE TABLE IF NOT EXISTS `IRRIGACOES` (
    `id_irrigacao` INT NOT NULL AUTO_INCREMENT,
    `id_area` INT NOT NULL,
    `id_usuario` INT NULL,
    `tipo_irrigacao` ENUM('AUTOMATICA', 'MANUAL') NOT NULL,
    `data_hora_inicio` DATETIME NOT NULL,
    `data_hora_fim` DATETIME NULL,
    `volume_agua_litros` DECIMAL(12,2) NOT NULL,
    `pressao_bar` DECIMAL(5,2) NULL,
    `metodo` ENUM('ASPERSAO', 'GOTEJAMENTO', 'PIVO') NOT NULL,
    `motivo` VARCHAR(100) NULL,
    `custo_estimado` DECIMAL(10,2) NULL,
    `status` ENUM('ATIVA', 'CONCLUIDA', 'CANCELADA') NOT NULL DEFAULT 'CONCLUIDA',
    `observacoes` TEXT NULL,
    
    PRIMARY KEY (`id_irrigacao`),
    INDEX `fk_irrigacoes_areas_idx` (`id_area` ASC),
    INDEX `fk_irrigacoes_usuarios_idx` (`id_usuario` ASC),
    INDEX `idx_data_inicio` (`data_hora_inicio` ASC),
    INDEX `idx_status_tipo` (`status` ASC, `tipo_irrigacao` ASC),
    
    -- Constraints
    CONSTRAINT `chk_volume_agua` CHECK (`volume_agua_litros` >= 0),
    CONSTRAINT `chk_pressao` CHECK (`pressao_bar` >= 0),
    CONSTRAINT `chk_datas_irrigacao` CHECK (`data_hora_fim` IS NULL OR `data_hora_fim` >= `data_hora_inicio`),
    
    -- Foreign Keys
    CONSTRAINT `fk_irrigacoes_areas`
        FOREIGN KEY (`id_area`)
        REFERENCES `AREAS_PLANTIO` (`id_area`)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_irrigacoes_usuarios`
        FOREIGN KEY (`id_usuario`)
        REFERENCES `USUARIOS` (`id_usuario`)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registros de irrigação das áreas';

-- ===============================================
-- TABELA: APLICACOES_NUTRIENTES
-- ===============================================
CREATE TABLE IF NOT EXISTS `APLICACOES_NUTRIENTES` (
    `id_aplicacao` INT NOT NULL AUTO_INCREMENT,
    `id_area` INT NOT NULL,
    `id_usuario` INT NULL,
    `tipo_nutriente` ENUM('FOSFORO', 'POTASSIO', 'NITROGENIO', 'NPK_COMPLETO') NOT NULL,
    `nome_produto` VARCHAR(100) NOT NULL,
    `quantidade_kg` DECIMAL(10,4) NOT NULL,
    `concentracao` VARCHAR(20) NULL,
    `data_hora_aplicacao` DATETIME NOT NULL,
    `metodo_aplicacao` ENUM('FOLIAR', 'SOLO', 'FERTIRRIGACAO') NOT NULL,
    `equipamento` VARCHAR(50) NULL,
    `custo_unitario` DECIMAL(10,2) NULL,
    `custo_total` DECIMAL(10,2) NULL,
    `observacoes` TEXT NULL,
    
    PRIMARY KEY (`id_aplicacao`),
    INDEX `fk_aplicacoes_areas_idx` (`id_area` ASC),
    INDEX `fk_aplicacoes_usuarios_idx` (`id_usuario` ASC),
    INDEX `idx_data_aplicacao` (`data_hora_aplicacao` ASC),
    INDEX `idx_tipo_nutriente` (`tipo_nutriente` ASC),
    
    -- Constraints
    CONSTRAINT `chk_quantidade_kg` CHECK (`quantidade_kg` > 0),
    CONSTRAINT `chk_custos` CHECK (`custo_unitario` >= 0 AND `custo_total` >= 0),
    
    -- Foreign Keys
    CONSTRAINT `fk_aplicacoes_areas`
        FOREIGN KEY (`id_area`)
        REFERENCES `AREAS_PLANTIO` (`id_area`)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT `fk_aplicacoes_usuarios`
        FOREIGN KEY (`id_usuario`)
        REFERENCES `USUARIOS` (`id_usuario`)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Registros de aplicação de nutrientes';

-- ===============================================
-- TABELA: ALERTAS
-- ===============================================
CREATE TABLE IF NOT EXISTS `ALERTAS` (
    `id_alerta` INT NOT NULL AUTO_INCREMENT,
    `id_area` INT NULL,
    `id_sensor` INT NULL,
    `id_usuario_destinatario` INT NULL,
    `tipo_alerta` ENUM('CRITICO', 'AVISO', 'INFO') NOT NULL,
    `categoria` ENUM('UMIDADE', 'PH', 'NUTRIENTE', 'SISTEMA', 'MANUTENCAO') NOT NULL,
    `titulo` VARCHAR(100) NOT NULL,
    `mensagem` TEXT NOT NULL,
    `valor_atual` DECIMAL(10,4) NULL,
    `valor_ideal` DECIMAL(10,4) NULL,
    `data_hora_alerta` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `data_hora_lido` DATETIME NULL,
    `data_hora_resolvido` DATETIME NULL,
    `status` ENUM('PENDENTE', 'LIDO', 'RESOLVIDO') NOT NULL DEFAULT 'PENDENTE',
    `acao_tomada` TEXT NULL,
    
    PRIMARY KEY (`id_alerta`),
    INDEX `fk_alertas_areas_idx` (`id_area` ASC),
    INDEX `fk_alertas_sensores_idx` (`id_sensor` ASC),
    INDEX `fk_alertas_usuarios_idx` (`id_usuario_destinatario` ASC),
    INDEX `idx_status_tipo` (`status` ASC, `tipo_alerta` ASC),
    INDEX `idx_data_alerta` (`data_hora_alerta` ASC),
    
    -- Foreign Keys
    CONSTRAINT `fk_alertas_areas`
        FOREIGN KEY (`id_area`)
        REFERENCES `AREAS_PLANTIO` (`id_area`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_alertas_sensores`
        FOREIGN KEY (`id_sensor`)
        REFERENCES `SENSORES` (`id_sensor`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_alertas_usuarios`
        FOREIGN KEY (`id_usuario_destinatario`)
        REFERENCES `USUARIOS` (`id_usuario`)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Sistema de alertas e notificações';

-- ===============================================
-- TABELA ASSOCIATIVA: USUARIOS_PROPRIEDADES (N:N)
-- ===============================================
CREATE TABLE IF NOT EXISTS `USUARIOS_PROPRIEDADES` (
    `id_usuario` INT NOT NULL,
    `id_propriedade` INT NOT NULL,
    `data_vinculo` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `tipo_acesso` ENUM('PROPRIETARIO', 'GESTOR', 'TECNICO', 'VISUALIZADOR') NOT NULL,
    `ativo` BOOLEAN NOT NULL DEFAULT TRUE,
    
    PRIMARY KEY (`id_usuario`, `id_propriedade`),
    INDEX `fk_up_propriedades_idx` (`id_propriedade` ASC),
    
    -- Foreign Keys
    CONSTRAINT `fk_up_usuarios`
        FOREIGN KEY (`id_usuario`)
        REFERENCES `USUARIOS` (`id_usuario`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_up_propriedades`
        FOREIGN KEY (`id_propriedade`)
        REFERENCES `PROPRIEDADES` (`id_propriedade`)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Relacionamento N:N entre usuários e propriedades';

-- ===============================================
-- VIEWS PARA CONSULTAS OTIMIZADAS
-- ===============================================

-- View: Resumo das áreas com informações consolidadas
CREATE OR REPLACE VIEW `VW_AREAS_RESUMO` AS
SELECT 
    ap.id_area,
    ap.nome_area,
    p.nome_propriedade,
    c.nome_cultura,
    u.nome_completo AS responsavel,
    ap.area_hectares,
    ap.status,
    ap.data_plantio,
    ap.data_previsao_colheita,
    COUNT(DISTINCT s.id_sensor) AS total_sensores,
    COUNT(DISTINCT CASE WHEN s.status = 'ATIVO' THEN s.id_sensor END) AS sensores_ativos
FROM AREAS_PLANTIO ap
JOIN PROPRIEDADES p ON ap.id_propriedade = p.id_propriedade
JOIN CULTURAS c ON ap.id_cultura = c.id_cultura
JOIN USUARIOS u ON ap.id_usuario_responsavel = u.id_usuario
LEFT JOIN SENSORES s ON ap.id_area = s.id_area
GROUP BY ap.id_area;

-- View: Últimas leituras dos sensores
CREATE OR REPLACE VIEW `VW_ULTIMAS_LEITURAS` AS
SELECT 
    s.id_sensor,
    s.tipo_sensor,
    s.modelo,
    ap.nome_area,
    ls.valor,
    ls.unidade,
    ls.data_hora_leitura,
    ls.qualidade_sinal,
    CASE 
        WHEN s.tipo_sensor = 'PH' AND (ls.valor < c.ph_ideal_min OR ls.valor > c.ph_ideal_max) THEN 'FORA_IDEAL'
        WHEN s.tipo_sensor = 'UMIDADE' AND (ls.valor < c.umidade_ideal_min OR ls.valor > c.umidade_ideal_max) THEN 'FORA_IDEAL'
        ELSE 'NORMAL'
    END AS status_leitura
FROM SENSORES s
JOIN AREAS_PLANTIO ap ON s.id_area = ap.id_area
JOIN CULTURAS c ON ap.id_cultura = c.id_cultura
JOIN LEITURAS_SENSORES ls ON s.id_sensor = ls.id_sensor
WHERE ls.data_hora_leitura = (
    SELECT MAX(data_hora_leitura) 
    FROM LEITURAS_SENSORES ls2 
    WHERE ls2.id_sensor = s.id_sensor
);

-- View: Estatísticas de irrigação por área
CREATE OR REPLACE VIEW `VW_ESTATISTICAS_IRRIGACAO` AS
SELECT 
    ap.id_area,
    ap.nome_area,
    COUNT(i.id_irrigacao) AS total_irrigacoes,
    SUM(i.volume_agua_litros) AS volume_total_litros,
    AVG(i.volume_agua_litros) AS volume_medio_litros,
    SUM(CASE WHEN i.tipo_irrigacao = 'AUTOMATICA' THEN 1 ELSE 0 END) AS irrigacoes_automaticas,
    SUM(CASE WHEN i.tipo_irrigacao = 'MANUAL' THEN 1 ELSE 0 END) AS irrigacoes_manuais,
    MAX(i.data_hora_inicio) AS ultima_irrigacao
FROM AREAS_PLANTIO ap
LEFT JOIN IRRIGACOES i ON ap.id_area = i.id_area
WHERE i.status = 'CONCLUIDA'
GROUP BY ap.id_area, ap.nome_area;

-- ===============================================
-- TRIGGERS PARA REGRAS DE NEGÓCIO
-- ===============================================

-- Trigger: Verificar se área colhida não pode receber irrigação
DELIMITER $$
CREATE TRIGGER `TRG_IRRIGACAO_AREA_COLHIDA` 
BEFORE INSERT ON `IRRIGACOES`
FOR EACH ROW
BEGIN
    DECLARE area_status VARCHAR(20);
    
    SELECT status INTO area_status 
    FROM AREAS_PLANTIO 
    WHERE id_area = NEW.id_area;
    
    IF area_status = 'COLHIDO' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Não é possível irrigar uma área já colhida';
    END IF;
END$$

-- Trigger: Criar alerta automático para leituras fora do padrão
CREATE TRIGGER `TRG_ALERTA_LEITURA_CRITICA` 
AFTER INSERT ON `LEITURAS_SENSORES`
FOR EACH ROW
BEGIN
    DECLARE v_ph_min, v_ph_max, v_umidade_min, v_umidade_max DECIMAL(10,4);
    DECLARE v_area_id INT;
    DECLARE v_usuario_responsavel INT;
    
    -- Buscar parâmetros ideais da cultura
    SELECT ap.id_area, ap.id_usuario_responsavel, 
           c.ph_ideal_min, c.ph_ideal_max, 
           c.umidade_ideal_min, c.umidade_ideal_max
    INTO v_area_id, v_usuario_responsavel, 
         v_ph_min, v_ph_max, v_umidade_min, v_umidade_max
    FROM SENSORES s
    JOIN AREAS_PLANTIO ap ON s.id_area = ap.id_area
    JOIN CULTURAS c ON ap.id_cultura = c.id_cultura
    WHERE s.id_sensor = NEW.id_sensor;
    
    -- Verificar pH crítico
    IF (SELECT tipo_sensor FROM SENSORES WHERE id_sensor = NEW.id_sensor) = 'PH' 
       AND (NEW.valor < v_ph_min OR NEW.valor > v_ph_max) THEN
        
        INSERT INTO ALERTAS (
            id_area, id_sensor, id_usuario_destinatario, 
            tipo_alerta, categoria, titulo, mensagem, 
            valor_atual, valor_ideal
        ) VALUES (
            v_area_id, NEW.id_sensor, v_usuario_responsavel,
            'CRITICO', 'PH', 'pH fora da faixa ideal',
            CONCAT('pH medido: ', NEW.valor, '. Faixa ideal: ', v_ph_min, ' - ', v_ph_max),
            NEW.valor, (v_ph_min + v_ph_max) / 2
        );
    END IF;
    
    -- Verificar umidade crítica
    IF (SELECT tipo_sensor FROM SENSORES WHERE id_sensor = NEW.id_sensor) = 'UMIDADE' 
       AND (NEW.valor < v_umidade_min OR NEW.valor > v_umidade_max) THEN
        
        INSERT INTO ALERTAS (
            id_area, id_sensor, id_usuario_destinatario,
            tipo_alerta, categoria, titulo, mensagem,
            valor_atual, valor_ideal
        ) VALUES (
            v_area_id, NEW.id_sensor, v_usuario_responsavel,
            'AVISO', 'UMIDADE', 'Umidade fora da faixa ideal',
            CONCAT('Umidade medida: ', NEW.valor, '%. Faixa ideal: ', v_umidade_min, '% - ', v_umidade_max, '%'),
            NEW.valor, (v_umidade_min + v_umidade_max) / 2
        );
    END IF;
END$$

DELIMITER ;

-- ===============================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- ===============================================

-- Índices compostos para consultas frequentes
CREATE INDEX `idx_leituras_sensor_data_valor` ON `LEITURAS_SENSORES` (`id_sensor`, `data_hora_leitura`, `valor`);
CREATE INDEX `idx_irrigacoes_area_data` ON `IRRIGACOES` (`id_area`, `data_hora_inicio`);
CREATE INDEX `idx_aplicacoes_area_data` ON `APLICACOES_NUTRIENTES` (`id_area`, `data_hora_aplicacao`);
CREATE INDEX `idx_alertas_usuario_status` ON `ALERTAS` (`id_usuario_destinatario`, `status`, `data_hora_alerta`);

-- ===============================================
-- PROCEDURES PARA OPERAÇÕES COMUNS
-- ===============================================

-- Procedure: Obter estatísticas de uma propriedade
DELIMITER $$
CREATE PROCEDURE `SP_ESTATISTICAS_PROPRIEDADE`(
    IN p_id_propriedade INT
)
BEGIN
    SELECT 
        p.nome_propriedade,
        p.area_total,
        COUNT(DISTINCT ap.id_area) AS total_areas,
        COUNT(DISTINCT s.id_sensor) AS total_sensores,
        COUNT(DISTINCT CASE WHEN ap.status = 'ATIVO' THEN ap.id_area END) AS areas_ativas,
        SUM(ap.area_hectares) AS area_plantada_total,
        COUNT(DISTINCT i.id_irrigacao) AS total_irrigacoes_mes,
        SUM(i.volume_agua_litros) AS agua_total_mes
    FROM PROPRIEDADES p
    LEFT JOIN AREAS_PLANTIO ap ON p.id_propriedade = ap.id_propriedade
    LEFT JOIN SENSORES s ON ap.id_area = s.id_area
    LEFT JOIN IRRIGACOES i ON ap.id_area = i.id_area 
        AND i.data_hora_inicio >= DATE_SUB(NOW(), INTERVAL 30 DAY)
    WHERE p.id_propriedade = p_id_propriedade
    GROUP BY p.id_propriedade;
END$$

-- Procedure: Processar leituras não processadas
CREATE PROCEDURE `SP_PROCESSAR_LEITURAS`()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_id_leitura BIGINT;
    DECLARE v_id_sensor INT;
    DECLARE v_valor DECIMAL(10,4);
    
    DECLARE cur CURSOR FOR 
        SELECT id_leitura, id_sensor, valor 
        FROM LEITURAS_SENSORES 
        WHERE processado = FALSE 
        LIMIT 1000;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO v_id_leitura, v_id_sensor, v_valor;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Marcar como processado
        UPDATE LEITURAS_SENSORES 
        SET processado = TRUE 
        WHERE id_leitura = v_id_leitura;
        
    END LOOP;
    
    CLOSE cur;
    
    SELECT CONCAT('Processadas ', ROW_COUNT(), ' leituras') AS resultado;
END$$

DELIMITER ;

-- ===============================================
-- CONFIGURAÇÕES FINAIS
-- ===============================================

-- Restaurar configurações
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- Comentários finais
SELECT 'Banco de dados FarmTech Solutions criado com sucesso!' AS status;
SELECT COUNT(*) AS total_tabelas FROM information_schema.tables WHERE table_schema = 'farmtech_solutions';