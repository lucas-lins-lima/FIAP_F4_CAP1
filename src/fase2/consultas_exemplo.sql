-- =====================================================
-- FarmTech Solutions - Consultas de Exemplo
-- Demonstração das funcionalidades do banco de dados
-- =====================================================

-- =====================================================
-- 1. CONSULTAS DE MONITORAMENTO DE SENSORES
-- =====================================================

-- Leituras de umidade dos últimos 7 dias
SELECT 
    f.nome_fazenda,
    c.nome_plantacao,
    c.tipo_cultura,
    l.valor_leitura as umidade,
    l.data_hora
FROM leitura_sensor l
JOIN sensor s ON l.id_sensor = s.id_sensor
JOIN cultura c ON s.id_cultura = c.id_cultura
JOIN fazenda f ON c.id_fazenda = f.id_fazenda
WHERE s.tipo_sensor = 'umidade'
  AND l.data_hora >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY l.data_hora DESC;

-- Variação do pH ao longo do tempo por cultura
SELECT 
    c.nome_plantacao,
    c.tipo_cultura,
    DATE(l.data_hora) as data_leitura,
    AVG(l.valor_leitura) as ph_medio,
    MIN(l.valor_leitura) as ph_minimo,
    MAX(l.valor_leitura) as ph_maximo,
    COUNT(*) as total_leituras
FROM leitura_sensor l
JOIN sensor s ON l.id_sensor = s.id_sensor
JOIN cultura c ON s.id_cultura = c.id_cultura
WHERE s.tipo_sensor = 'pH'
GROUP BY c.id_cultura, DATE(l.data_hora)
ORDER BY c.nome_plantacao, data_leitura;

-- Status atual dos sensores por fazenda
SELECT 
    f.nome_fazenda,
    s.tipo_sensor,
    COUNT(*) as total_sensores,
    SUM(CASE WHEN s.status_sensor = 'Ativo' THEN 1 ELSE 0 END) as sensores_ativos,
    SUM(CASE WHEN s.status_sensor = 'Inativo' THEN 1 ELSE 0 END) as sensores_inativos,
    SUM(CASE WHEN s.status_sensor = 'Manutenção' THEN 1 ELSE 0 END) as sensores_manutencao
FROM sensor s
JOIN cultura c ON s.id_cultura = c.id_cultura
JOIN fazenda f ON c.id_fazenda = f.id_fazenda
GROUP BY f.id_fazenda, s.tipo_sensor
ORDER BY f.nome_fazenda;

-- =====================================================
-- 2. RELATÓRIOS DE IRRIGAÇÃO
-- =====================================================

-- Consumo total de água por mês
SELECT 
    f.nome_fazenda,
    c.nome_plantacao,
    YEAR(ai.data_hora_inicio) as ano,
    MONTH(ai.data_hora_inicio) as mes,
    SUM(ai.quantidade_agua) as total_agua_litros,
    COUNT(*) as total_acionamentos,
    AVG(ai.quantidade_agua) as media_por_acionamento
FROM acionamento_irrigacao ai
JOIN sistema_irrigacao si ON ai.id_irrigacao = si.id_irrigacao
JOIN cultura c ON si.id_cultura = c.id_cultura
JOIN fazenda f ON c.id_fazenda = f.id_fazenda
WHERE ai.quantidade_agua IS NOT NULL
GROUP BY f.id_fazenda, c.id_cultura, YEAR(ai.data_hora_inicio), MONTH(ai.data_hora_inicio)
ORDER BY f.nome_fazenda, ano, mes;

-- Eficiência da irrigação (comparando umidade antes e depois)
SELECT 
    c.nome_plantacao,
    c.tipo_cultura,
    AVG(ai.umidade_antes) as umidade_media_antes,
    AVG(ai.umidade_depois) as umidade_media_depois,
    AVG(ai.umidade_depois - ai.umidade_antes) as ganho_medio_umidade,
    AVG(ai.quantidade_agua) as agua_media_por_irrigacao
FROM acionamento_irrigacao ai
JOIN sistema_irrigacao si ON ai.id_irrigacao = si.id_irrigacao
JOIN cultura c ON si.id_cultura = c.id_cultura
WHERE ai.umidade_antes IS NOT NULL 
  AND ai.umidade_depois IS NOT NULL
GROUP BY c.id_cultura
ORDER BY ganho_medio_umidade DESC;

-- =====================================================
-- 3. ANÁLISE DE INSUMOS
-- =====================================================

-- Custo total de insumos por cultura no último ano
SELECT 
    f.nome_fazenda,
    c.nome_plantacao,
    c.tipo_cultura,
    SUM(ap.custo_total) as custo_total_insumos,
    COUNT(*) as total_aplicacoes,
    AVG(ap.custo_total) as custo_medio_aplicacao
FROM aplicacao_insumo ap
JOIN cultura c ON ap.id_cultura = c.id_cultura
JOIN fazenda f ON c.id_fazenda = f.id_fazenda
WHERE ap.data_aplicacao >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
  AND ap.custo_total IS NOT NULL
GROUP BY c.id_cultura
ORDER BY custo_total_insumos DESC;

-- Insumos mais utilizados por tipo de cultura
SELECT 
    c.tipo_cultura,
    i.nome_insumo,
    i.tipo_insumo,
    COUNT(*) as total_aplicacoes,
    SUM(ap.quantidade_aplicada) as quantidade_total,
    AVG(ap.quantidade_aplicada) as quantidade_media
FROM aplicacao_insumo ap
JOIN cultura c ON ap.id_cultura = c.id_cultura
JOIN insumo i ON ap.id_insumo = i.id_insumo
GROUP BY c.tipo_cultura, i.id_insumo
ORDER BY c.tipo_cultura, total_aplicacoes DESC;

-- =====================================================
-- 4. RELATÓRIOS EXECUTIVOS
-- =====================================================

-- Dashboard executivo por fazenda
SELECT 
    f.nome_fazenda,
    f.proprietario,
    f.area_total,
    COUNT(DISTINCT c.id_cultura) as total_culturas,
    SUM(c.area_plantada) as area_cultivada,
    ROUND((SUM(c.area_plantada) / f.area_total) * 100, 2) as percentual_uso,
    COUNT(DISTINCT s.id_sensor) as total_sensores,
    COUNT(DISTINCT si.id_irrigacao) as total_sistemas_irrigacao
FROM fazenda f
LEFT JOIN cultura c ON f.id_fazenda = c.id_fazenda
LEFT JOIN sensor s ON c.id_cultura = s.id_cultura
LEFT JOIN sistema_irrigacao si ON c.id_cultura = si.id_cultura
GROUP BY f.id_fazenda
ORDER BY area_cultivada DESC;

-- Análise de produtividade por tipo de cultura
SELECT 
    c.tipo_cultura,
    COUNT(*) as total_plantacoes,
    SUM(c.area_plantada) as area_total,
    AVG(c.area_plantada) as area_media,
    -- Simulação de produtividade baseada nos dados da Fase 1
    CASE 
        WHEN c.tipo_cultura = 'Café' THEN SUM(c.area_plantada) * 0.8
        WHEN c.tipo_cultura = 'Milho' THEN SUM(c.area_plantada) * 1.2
        WHEN c.tipo_cultura = 'Soja' THEN SUM(c.area_plantada) * 0.9
        ELSE SUM(c.area_plantada) * 1.0
    END as producao_estimada_kg
FROM cultura c
WHERE c.status_cultura = 'Ativa'
GROUP BY c.tipo_cultura
ORDER BY producao_estimada_kg DESC;

-- =====================================================
-- 5. ALERTAS E MONITORAMENTO
-- =====================================================

-- Sensores que não enviaram dados nas últimas 24 horas
SELECT 
    f.nome_fazenda,
    c.nome_plantacao,
    s.tipo_sensor,
    s.modelo_sensor,
    s.status_sensor,
    MAX(l.data_hora) as ultima_leitura,
    TIMESTAMPDIFF(HOUR, MAX(l.data_hora), NOW()) as horas_sem_dados
FROM sensor s
JOIN cultura c ON s.id_cultura = c.id_cultura
JOIN fazenda f ON c.id_fazenda = f.id_fazenda
LEFT JOIN leitura_sensor l ON s.id_sensor = l.id_sensor
WHERE s.status_sensor = 'Ativo'
GROUP BY s.id_sensor
HAVING MAX(l.data_hora) < DATE_SUB(NOW(), INTERVAL 24 HOUR) 
    OR MAX(l.data_hora) IS NULL
ORDER BY horas_sem_dados DESC;

-- Culturas com níveis críticos de umidade
SELECT 
    f.nome_fazenda,
    c.nome_plantacao,
    c.tipo_cultura,
    l.valor_leitura as umidade_atual,
    l.data_hora as ultima_medicao,
    CASE 
        WHEN l.valor_leitura < 20 THEN 'CRÍTICO'
        WHEN l.valor_leitura < 30 THEN 'BAIXO'
        WHEN l.valor_leitura > 80 THEN 'ALTO'
        ELSE 'NORMAL'
    END as status_umidade
FROM leitura_sensor l
JOIN sensor s ON l.id_sensor = s.id_sensor
JOIN cultura c ON s.id_cultura = c.id_cultura
JOIN fazenda f ON c.id_fazenda = f.id_fazenda
WHERE s.tipo_sensor = 'umidade'
  AND l.data_hora = (
    SELECT MAX(l2.data_hora) 
    FROM leitura_sensor l2 
    WHERE l2.id_sensor = l.id_sensor
  )
  AND (l.valor_leitura < 30 OR l.valor_leitura > 80)
ORDER BY l.valor_leitura;
