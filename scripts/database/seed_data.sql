-- ===============================================
-- FarmTech Solutions - Dados de Exemplo
-- Populando o banco com dados de demonstração
-- ===============================================

USE `farmtech_solutions`;

-- ===============================================
-- INSERÇÃO DE DADOS BÁSICOS
-- ===============================================

-- Inserir Culturas
INSERT INTO `CULTURAS` (nome_cultura, nome_cientifico, ph_ideal_min, ph_ideal_max, umidade_ideal_min, umidade_ideal_max, fosforo_ideal, potassio_ideal, ciclo_dias, descricao) VALUES
('Soja', 'Glycine max', 6.0, 7.0, 60.0, 80.0, 15.0, 120.0, 120, 'Leguminosa rica em proteínas, importante para o agronegócio brasileiro'),
('Milho', 'Zea mays', 5.8, 7.0, 65.0, 85.0, 20.0, 150.0, 140, 'Cereal versátil usado na alimentação humana e animal'),
('Café', 'Coffea arabica', 6.0, 6.8, 70.0, 85.0, 25.0, 180.0, 300, 'Cultura perene de grande importância econômica'),
('Cana-de-açúcar', 'Saccharum officinarum', 5.5, 6.5, 75.0, 90.0, 18.0, 140.0, 365, 'Matéria-prima do açúcar e etanol');

-- Inserir Usuários
INSERT INTO `USUARIOS` (nome_completo, email, telefone, tipo_usuario, data_nascimento) VALUES
('João Silva Santos', 'joao.silva@fazenda.com', '(11) 99999-1111', 'PROPRIETARIO', '1975-03-15'),
('Maria Oliveira Costa', 'maria.oliveira@farmtech.com', '(11) 99999-2222', 'TECNICO', '1985-07-22'),
('Pedro Almeida Souza', 'pedro.almeida@fazenda.com', '(11) 99999-3333', 'PROPRIETARIO', '1970-11-08'),
('Ana Carolina Lima', 'ana.lima@farmtech.com', '(11) 99999-4444', 'ADMINISTRADOR', '1990-02-14'),
('Carlos Eduardo Ferreira', 'carlos.ferreira@tecnico.com', '(11) 99999-5555', 'TECNICO', '1988-09-30');

-- Inserir Propriedades
INSERT INTO `PROPRIEDADES` (nome_propriedade, endereco, cidade, estado, cep, area_total, latitude, longitude) VALUES
('Fazenda São João', 'Rodovia BR-364, Km 45', 'Cuiabá', 'MT', '78000-000', 1250.50, -15.5989, -56.0949),
('Sítio Esperança', 'Estrada Municipal 120, s/n', 'Ribeirão Preto', 'SP', '14000-000', 850.75, -21.1775, -47.8208),
('Fazenda Monte Verde', 'Rodovia MG-050, Km 180', 'Passos', 'MG', '37900-000', 650.25, -20.7187, -46.6097),
('Propriedade Doce Vida', 'Rodovia GO-164, Km 25', 'Rio Verde', 'GO', '75900-000', 980.00, -17.7979, -50.9264);

-- Relacionar Usuários com Propriedades
INSERT INTO `USUARIOS_PROPRIEDADES` (id_usuario, id_propriedade, tipo_acesso) VALUES
(1, 1, 'PROPRIETARIO'),
(2, 1, 'TECNICO'),
(3, 2, 'PROPRIETARIO'),
(2, 2, 'TECNICO'),
(1, 3, 'PROPRIETARIO'),
(4, 1, 'GESTOR'),
(4, 2, 'GESTOR'),
(5, 3, 'TECNICO'),
(5, 4, 'TECNICO');

-- Inserir Áreas de Plantio
INSERT INTO `AREAS_PLANTIO` (id_propriedade, id_cultura, id_usuario_responsavel, nome_area, geometria, area_hectares, data_plantio, data_previsao_colheita, observacoes) VALUES
(1, 1, 1, 'Lote A - Soja Precoce', 'RETANGULAR', 125.50, '2024-10-15', '2025-02-15', 'Área com sistema de irrigação por pivô central'),
(1, 2, 1, 'Lote B - Milho Safrinha', 'CIRCULAR', 95.25, '2024-03-01', '2024-07-20', 'Plantio de segunda safra após soja'),
(2, 1, 3, 'Quadra 1 - Soja', 'RETANGULAR', 200.00, '2024-11-01', '2025-03-01', 'Primeira safra da propriedade'),
(2, 3, 3, 'Cafezal Sul', 'TRAPEZOIDAL', 45.75, '2023-05-15', '2024-05-15', 'Café arábica plantado em terreno montanhoso'),
(3, 3, 1, 'Cafezal Norte', 'TRAPEZOIDAL', 80.50, '2022-06-01', '2024-06-01', 'Área com sombreamento natural'),
(4, 4, 5, 'Talhão 1 - Cana', 'TRIANGULAR', 150.00, '2024-04-01', '2025-04-01', 'Primeiro corte da cana-de-açúcar');

-- Inserir Sensores
INSERT INTO `SENSORES` (id_area, tipo_sensor, modelo, numero_serie, localizacao_x, localizacao_y, profundidade_cm, data_instalacao, intervalo_leitura_min) VALUES
-- Lote A - Soja
(1, 'UMIDADE', 'DHT22-AgriSense', 'DHT-001-2024', 62.75, 125.25, 15, '2024-10-10', 15),
(1, 'PH', 'pHMeter-Pro-300', 'PHM-001-2024', 62.75, 125.25, 20, '2024-10-10', 30),
(1, 'FOSFORO', 'NutriSense-P', 'NSP-001-2024', 62.75, 125.25, 25, '2024-10-10', 60),
(1, 'POTASSIO', 'NutriSense-K', 'NSK-001-2024', 62.75, 125.25, 25, '2024-10-10', 60),

-- Lote B - Milho
(2, 'UMIDADE', 'DHT22-AgriSense', 'DHT-002-2024', 47.62, 47.62, 15, '2024-02-25', 15),
(2, 'PH', 'pHMeter-Pro-300', 'PHM-002-2024', 47.62, 47.62, 20, '2024-02-25', 30),
(2, 'FOSFORO', 'NutriSense-P', 'NSP-002-2024', 47.62, 47.62, 25, '2024-02-25', 60),
(2, 'POTASSIO', 'NutriSense-K', 'NSK-002-2024', 47.62, 47.62, 25, '2024-02-25', 60),

-- Quadra 1 - Soja
(3, 'UMIDADE', 'DHT22-AgriSense', 'DHT-003-2024', 100.00, 100.00, 15, '2024-10-25', 15),
(3, 'PH', 'pHMeter-Pro-300', 'PHM-003-2024', 100.00, 100.00, 20, '2024-10-25', 30),

-- Cafezal Sul
(4, 'UMIDADE', 'DHT22-AgriSense', 'DHT-004-2024', 22.87, 30.00, 10, '2023-05-10', 20),
(4, 'PH', 'pHMeter-Pro-300', 'PHM-004-2024', 22.87, 30.00, 15, '2023-05-10', 45);

-- Inserir Leituras dos Sensores (últimos 7 dias)
INSERT INTO `LEITURAS_SENSORES` (id_sensor, valor, unidade, data_hora_leitura, qualidade_sinal, temperatura_ambiente) VALUES
-- Sensor de Umidade Lote A (últimas 24h, a cada 15 min)
(1, 72.5, '%', '2024-12-09 00:00:00', 98, 22.1),
(1, 71.8, '%', '2024-12-09 00:15:00', 99, 21.8),
(1, 71.2, '%', '2024-12-09 00:30:00', 97, 21.5),
(1, 70.9, '%', '2024-12-09 00:45:00', 98, 21.2),
(1, 70.5, '%', '2024-12-09 01:00:00', 99, 20.9),

-- Sensor de pH Lote A (últimas 12h, a cada 30 min)
(2, 6.4, 'pH', '2024-12-08 12:00:00', 95, 24.5),
(2, 6.3, 'pH', '2024-12-08 12:30:00', 96, 25.1),
(2, 6.5, 'pH', '2024-12-08 13:00:00', 94, 25.8),
(2, 6.2, 'pH', '2024-12-08 13:30:00', 97, 26.2),
(2, 6.1, 'pH', '2024-12-08 14:00:00', 93, 26.8),

-- Sensor de Fósforo Lote A (últimas 6h, a cada 60 min)
(3, 16.2, 'mg/dm³', '2024-12-08 09:00:00', 92, 23.5),
(3, 15.8, 'mg/dm³', '2024-12-08 10:00:00', 94, 24.2),
(3, 16.5, 'mg/dm³', '2024-12-08 11:00:00', 91, 24.8),
(3, 16.0, 'mg/dm³', '2024-12-08 12:00:00', 93, 25.1),

-- Sensor de Potássio Lote A
(4, 125.5, 'mg/dm³', '2024-12-08 09:00:00', 89, 23.5),
(4, 127.2, 'mg/dm³', '2024-12-08 10:00:00', 91, 24.2),
(4, 124.8, 'mg/dm³', '2024-12-08 11:00:00', 88, 24.8),
(4, 126.1, 'mg/dm³', '2024-12-08 12:00:00', 90, 25.1);

-- Inserir Irrigações
INSERT INTO `IRRIGACOES` (id_area, id_usuario, tipo_irrigacao, data_hora_inicio, data_hora_fim, volume_agua_litros, pressao_bar, metodo, motivo, custo_estimado, observacoes) VALUES
(1, 1, 'AUTOMATICA', '2024-12-07 06:00:00', '2024-12-07 08:30:00', 15000.00, 2.5, 'PIVO', 'Baixa umidade detectada pelos sensores', 450.00, 'Irrigação automática acionada por umidade < 65%'),
(1, 2, 'MANUAL', '2024-12-05 16:00:00', '2024-12-05 18:00:00', 12000.00, 2.8, 'PIVO', 'Irrigação preventiva antes do período seco', 360.00, 'Irrigação manual programada'),
(2, 1, 'AUTOMATICA', '2024-12-06 05:30:00', '2024-12-06 07:00:00', 8500.00, 2.2, 'ASPERSAO', 'Umidade baixa', 255.00, NULL),
(3, 3, 'MANUAL', '2024-12-04 14:00:00', '2024-12-04 16:30:00', 20000.00, 3.0, 'ASPERSAO', 'Irrigação semanal programada', 600.00, 'Área maior necessita mais água');

-- Inserir Aplicações de Nutrientes
INSERT INTO `APLICACOES_NUTRIENTES` (id_area, id_usuario, tipo_nutriente, nome_produto, quantidade_kg, concentracao, data_hora_aplicacao, metodo_aplicacao, equipamento, custo_unitario, custo_total, observacoes) VALUES
(1, 2, 'FOSFORO', 'Superfosfato Simples', 125.50, '18% P2O5', '2024-10-20 08:00:00', 'SOLO', 'Distribuidor a Lanço', 2.50, 313.75, 'Aplicação na base do plantio'),
(1, 2, 'POTASSIO', 'Cloreto de Potássio', 95.00, '60% K2O', '2024-11-15 09:30:00', 'SOLO', 'Distribuidor a Lanço', 3.20, 304.00, 'Aplicação em cobertura'),
(2, 2, 'NPK_COMPLETO', 'NPK 04-14-08', 200.00, 'NPK', '2024-03-05 07:00:00', 'SOLO', 'Plantadeira', 2.80, 560.00, 'Aplicação no sulco de plantio'),
(3, 3, 'NITROGENIO', 'Ureia', 180.00, '45% N', '2024-11-10 06:30:00', 'SOLO', 'Distribuidor Pendular', 2.10, 378.00, 'Cobertura nitrogenada'),
(4, 5, 'FOSFORO', 'Fosfato Monoamônico', 85.00, '48% P2O5', '2024-06-01 08:00:00', 'FERTIRRIGACAO', 'Sistema de Fertirrigação', 4.50, 382.50, 'Aplicação via água de irrigação');

-- Inserir Alertas
INSERT INTO `ALERTAS` (id_area, id_sensor, id_usuario_destinatario, tipo_alerta, categoria, titulo, mensagem, valor_atual, valor_ideal, status) VALUES
(1, 2, 1, 'AVISO', 'PH', 'pH abaixo do ideal', 'O sensor de pH detectou valor de 6.1, abaixo da faixa ideal para soja (6.0-7.0)', 6.1, 6.5, 'LIDO'),
(1, 1, 1, 'CRITICO', 'UMIDADE', 'Umidade crítica detectada', 'Umidade do solo em 58%, abaixo do mínimo recomendado de 60%', 58.0, 70.0, 'RESOLVIDO'),
(2, 5, 1, 'INFO', 'UMIDADE', 'Umidade normalizada', 'Após irrigação, umidade retornou ao nível adequado', 72.0, 75.0, 'LIDO'),
(3, 9, 3, 'AVISO', 'UMIDADE', 'Umidade baixa', 'Sensor detectou umidade de 62%, próximo ao limite mínimo', 62.0, 70.0, 'PENDENTE');

-- ===============================================
-- ATUALIZAR DADOS PROCESSADOS
-- ===============================================

-- Marcar algumas leituras como processadas
UPDATE `LEITURAS_SENSORES` SET processado = TRUE WHERE id_leitura <= 10;

-- Atualizar último acesso dos usuários
UPDATE `USUARIOS` SET ultimo_acesso = NOW() WHERE id_usuario IN (1, 2, 3);

-- ===============================================
-- VERIFICAÇÃO DOS DADOS INSERIDOS
-- ===============================================

SELECT 'Dados de exemplo inseridos com sucesso!' AS status;

SELECT 
    'Propriedades' AS tabela, COUNT(*) AS registros FROM PROPRIEDADES
UNION ALL SELECT 'Usuários', COUNT(*) FROM USUARIOS
UNION ALL SELECT 'Culturas', COUNT(*) FROM CULTURAS  
UNION ALL SELECT 'Áreas de Plantio', COUNT(*) FROM AREAS_PLANTIO
UNION ALL SELECT 'Sensores', COUNT(*) FROM SENSORES
UNION ALL SELECT 'Leituras', COUNT(*) FROM LEITURAS_SENSORES
UNION ALL SELECT 'Irrigações', COUNT(*) FROM IRRIGACOES
UNION ALL SELECT 'Aplicações Nutrientes', COUNT(*) FROM APLICACOES_NUTRIENTES
UNION ALL SELECT 'Alertas', COUNT(*) FROM ALERTAS;