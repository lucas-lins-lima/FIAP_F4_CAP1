# 🌾 MER - FarmTech Solutions Sistema de Sensoriamento Agrícola

## 📋 Modelo Entidade-Relacionamento (MER)

### **Versão:** 2.0
### **Data:**  2025
### **Equipe:** FarmTech Solutions Development Team

---

## 🎯 **Objetivo do Sistema**

Desenvolver um banco de dados robusto para gerenciar um sistema de sensoriamento agrícola inteligente que monitore em tempo real:
- Umidade do solo
- Níveis de pH
- Nutrientes (Fósforo e Potássio)
- Controle automatizado de irrigação
- Aplicação de nutrientes

---

## 🏗️ **ENTIDADES E ATRIBUTOS**

### **1. PROPRIEDADES**
**Descrição:** Fazendas/propriedades rurais cadastradas no sistema

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_propriedade` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `nome_propriedade` | VARCHAR | 100 | NOT NULL | Nome da fazenda |
| `endereco` | VARCHAR | 200 | NOT NULL | Endereço completo |
| `cidade` | VARCHAR | 50 | NOT NULL | Cidade |
| `estado` | VARCHAR | 2 | NOT NULL | UF do estado |
| `cep` | VARCHAR | 10 | NOT NULL | CEP |
| `area_total` | DECIMAL | 10,2 | NOT NULL, > 0 | Área total em hectares |
| `latitude` | DECIMAL | 10,8 | - | Coordenada GPS |
| `longitude` | DECIMAL | 11,8 | - | Coordenada GPS |
| `data_cadastro` | DATETIME | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de cadastro |
| `ativo` | BOOLEAN | - | NOT NULL, DEFAULT TRUE | Status ativo/inativo |

### **2. USUARIOS**
**Descrição:** Produtores rurais e técnicos que operam o sistema

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_usuario` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `nome_completo` | VARCHAR | 100 | NOT NULL | Nome completo |
| `email` | VARCHAR | 100 | NOT NULL, UNIQUE | Email para login |
| `telefone` | VARCHAR | 20 | - | Telefone contato |
| `tipo_usuario` | ENUM | - | NOT NULL | 'PROPRIETARIO', 'TECNICO', 'ADMINISTRADOR' |
| `data_nascimento` | DATE | - | - | Data de nascimento |
| `data_cadastro` | DATETIME | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de cadastro |
| `ultimo_acesso` | DATETIME | - | - | Último acesso ao sistema |
| `ativo` | BOOLEAN | - | NOT NULL, DEFAULT TRUE | Status ativo/inativo |

### **3. CULTURAS**
**Descrição:** Tipos de cultura/plantio suportados pelo sistema

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_cultura` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `nome_cultura` | VARCHAR | 50 | NOT NULL, UNIQUE | Nome da cultura |
| `nome_cientifico` | VARCHAR | 100 | - | Nome científico |
| `ph_ideal_min` | DECIMAL | 3,1 | NOT NULL, >= 0, <= 14 | pH mínimo ideal |
| `ph_ideal_max` | DECIMAL | 3,1 | NOT NULL, >= 0, <= 14 | pH máximo ideal |
| `umidade_ideal_min` | DECIMAL | 5,2 | NOT NULL, >= 0, <= 100 | Umidade mínima ideal (%) |
| `umidade_ideal_max` | DECIMAL | 5,2 | NOT NULL, >= 0, <= 100 | Umidade máxima ideal (%) |
| `fosforo_ideal` | DECIMAL | 6,2 | NOT NULL, >= 0 | Fósforo ideal (mg/dm³) |
| `potassio_ideal` | DECIMAL | 6,2 | NOT NULL, >= 0 | Potássio ideal (mg/dm³) |
| `ciclo_dias` | INTEGER | - | NOT NULL, > 0 | Ciclo da cultura em dias |
| `descricao` | TEXT | - | - | Descrição detalhada |
| `data_cadastro` | DATETIME | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de cadastro |

### **4. AREAS_PLANTIO**
**Descrição:** Áreas específicas dentro das propriedades onde há plantio

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_area` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `id_propriedade` | INTEGER | - | **FK, NOT NULL** | Referencia PROPRIEDADES |
| `id_cultura` | INTEGER | - | **FK, NOT NULL** | Referencia CULTURAS |
| `id_usuario_responsavel` | INTEGER | - | **FK, NOT NULL** | Responsável pela área |
| `nome_area` | VARCHAR | 100 | NOT NULL | Nome identificador da área |
| `geometria` | ENUM | - | NOT NULL | 'RETANGULAR', 'CIRCULAR', 'TRAPEZOIDAL', 'TRIANGULAR' |
| `area_hectares` | DECIMAL | 10,4 | NOT NULL, > 0 | Área em hectares |
| `coordenadas_json` | JSON | - | - | Coordenadas dos vértices |
| `data_plantio` | DATE | - | NOT NULL | Data do plantio |
| `data_previsao_colheita` | DATE | - | NOT NULL | Data prevista colheita |
| `status` | ENUM | - | NOT NULL, DEFAULT 'ATIVO' | 'ATIVO', 'INATIVO', 'COLHIDO' |
| `observacoes` | TEXT | - | - | Observações adicionais |
| `data_cadastro` | DATETIME | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de cadastro |

### **5. SENSORES**
**Descrição:** Dispositivos físicos de monitoramento

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_sensor` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `id_area` | INTEGER | - | **FK, NOT NULL** | Referencia AREAS_PLANTIO |
| `tipo_sensor` | ENUM | - | NOT NULL | 'UMIDADE', 'PH', 'FOSFORO', 'POTASSIO' |
| `modelo` | VARCHAR | 50 | NOT NULL | Modelo do sensor |
| `numero_serie` | VARCHAR | 50 | UNIQUE | Número de série |
| `localizacao_x` | DECIMAL | 8,4 | - | Posição X na área |
| `localizacao_y` | DECIMAL | 8,4 | - | Posição Y na área |
| `profundidade_cm` | INTEGER | - | - | Profundidade instalação (cm) |
| `data_instalacao` | DATE | - | NOT NULL | Data de instalação |
| `data_ultima_manutencao` | DATE | - | - | Última manutenção |
| `intervalo_leitura_min` | INTEGER | - | NOT NULL, DEFAULT 15 | Intervalo leituras (min) |
| `status` | ENUM | - | NOT NULL, DEFAULT 'ATIVO' | 'ATIVO', 'INATIVO', 'MANUTENCAO' |
| `data_cadastro` | DATETIME | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Data de cadastro |

### **6. LEITURAS_SENSORES**
**Descrição:** Dados coletados pelos sensores em tempo real

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_leitura` | BIGINT | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `id_sensor` | INTEGER | - | **FK, NOT NULL** | Referencia SENSORES |
| `valor` | DECIMAL | 10,4 | NOT NULL | Valor lido pelo sensor |
| `unidade` | VARCHAR | 10 | NOT NULL | Unidade de medida |
| `data_hora_leitura` | DATETIME | - | NOT NULL | Timestamp da leitura |
| `qualidade_sinal` | INTEGER | - | DEFAULT 100 | Qualidade sinal (0-100%) |
| `temperatura_ambiente` | DECIMAL | 5,2 | - | Temperatura no momento |
| `observacoes` | VARCHAR | 255 | - | Observações adicionais |
| `processado` | BOOLEAN | - | NOT NULL, DEFAULT FALSE | Se foi processado |

**Índices:** 
- `idx_sensor_data` (id_sensor, data_hora_leitura)
- `idx_data_hora` (data_hora_leitura)

### **7. IRRIGACOES**
**Descrição:** Registros de aplicação de água

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_irrigacao` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `id_area` | INTEGER | - | **FK, NOT NULL** | Referencia AREAS_PLANTIO |
| `id_usuario` | INTEGER | - | **FK** | Usuário que iniciou |
| `tipo_irrigacao` | ENUM | - | NOT NULL | 'AUTOMATICA', 'MANUAL' |
| `data_hora_inicio` | DATETIME | - | NOT NULL | Início da irrigação |
| `data_hora_fim` | DATETIME | - | - | Fim da irrigação |
| `volume_agua_litros` | DECIMAL | 12,2 | NOT NULL, >= 0 | Volume aplicado |
| `pressao_bar` | DECIMAL | 5,2 | - | Pressão da água |
| `metodo` | ENUM | - | NOT NULL | 'ASPERSAO', 'GOTEJAMENTO', 'PIVO' |
| `motivo` | VARCHAR | 100 | - | Motivo da irrigação |
| `custo_estimado` | DECIMAL | 10,2 | - | Custo estimado |
| `status` | ENUM | - | NOT NULL, DEFAULT 'CONCLUIDA' | 'ATIVA', 'CONCLUIDA', 'CANCELADA' |
| `observacoes` | TEXT | - | - | Observações |

### **8. APLICACOES_NUTRIENTES**
**Descrição:** Registros de aplicação de fertilizantes/nutrientes

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_aplicacao` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `id_area` | INTEGER | - | **FK, NOT NULL** | Referencia AREAS_PLANTIO |
| `id_usuario` | INTEGER | - | **FK** | Usuário responsável |
| `tipo_nutriente` | ENUM | - | NOT NULL | 'FOSFORO', 'POTASSIO', 'NITROGENIO', 'NPK_COMPLETO' |
| `nome_produto` | VARCHAR | 100 | NOT NULL | Nome comercial |
| `quantidade_kg` | DECIMAL | 10,4 | NOT NULL, > 0 | Quantidade aplicada |
| `concentracao` | VARCHAR | 20 | - | Concentração do produto |
| `data_hora_aplicacao` | DATETIME | - | NOT NULL | Data/hora aplicação |
| `metodo_aplicacao` | ENUM | - | NOT NULL | 'FOLIAR', 'SOLO', 'FERTIRRIGACAO' |
| `equipamento` | VARCHAR | 50 | - | Equipamento utilizado |
| `custo_unitario` | DECIMAL | 10,2 | - | Custo por kg |
| `custo_total` | DECIMAL | 10,2 | - | Custo total |
| `observacoes` | TEXT | - | - | Observações |

### **9. ALERTAS**
**Descrição:** Notificações automáticas do sistema

| Atributo | Tipo | Tamanho | Restrições | Descrição |
|----------|------|---------|------------|-----------|
| `id_alerta` | INTEGER | - | **PK, NOT NULL, AUTO_INCREMENT** | Identificador único |
| `id_area` | INTEGER | - | **FK** | Área relacionada |
| `id_sensor` | INTEGER | - | **FK** | Sensor que gerou alerta |
| `id_usuario_destinatario` | INTEGER | - | **FK** | Usuário destinatário |
| `tipo_alerta` | ENUM | - | NOT NULL | 'CRITICO', 'AVISO', 'INFO' |
| `categoria` | ENUM | - | NOT NULL | 'UMIDADE', 'PH', 'NUTRIENTE', 'SISTEMA', 'MANUTENCAO' |
| `titulo` | VARCHAR | 100 | NOT NULL | Título do alerta |
| `mensagem` | TEXT | NOT NULL | - | Mensagem detalhada |
| `valor_atual` | DECIMAL | 10,4 | - | Valor que gerou alerta |
| `valor_ideal` | DECIMAL | 10,4 | - | Valor ideal esperado |
| `data_hora_alerta` | DATETIME | - | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp do alerta |
| `data_hora_lido` | DATETIME | - | - | Quando foi lido |
| `data_hora_resolvido` | DATETIME | - | - | Quando foi resolvido |
| `status` | ENUM | - | NOT NULL, DEFAULT 'PENDENTE' | 'PENDENTE', 'LIDO', 'RESOLVIDO' |
| `acao_tomada` | TEXT | - | - | Ação tomada pelo usuário |

---

## 🔗 **RELACIONAMENTOS E CARDINALIDADES**

### **1. PROPRIEDADES ↔ USUARIOS**
- **Relacionamento:** N:N (Muitos para Muitos)
- **Entidade Associativa:** USUARIOS_PROPRIEDADES
- **Cardinalidade:** Uma propriedade pode ter vários usuários, um usuário pode gerenciar várias propriedades
- **Atributos da Associação:** data_vinculo, tipo_acesso, ativo

### **2. PROPRIEDADES ↔ AREAS_PLANTIO**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Uma propriedade tem várias áreas de plantio
- **Chave Estrangeira:** id_propriedade em AREAS_PLANTIO

### **3. CULTURAS ↔ AREAS_PLANTIO**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Uma cultura pode estar em várias áreas
- **Chave Estrangeira:** id_cultura em AREAS_PLANTIO

### **4. AREAS_PLANTIO ↔ SENSORES**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Uma área tem vários sensores
- **Chave Estrangeira:** id_area em SENSORES

### **5. SENSORES ↔ LEITURAS_SENSORES**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Um sensor gera várias leituras
- **Chave Estrangeira:** id_sensor em LEITURAS_SENSORES

### **6. AREAS_PLANTIO ↔ IRRIGACOES**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Uma área pode ter várias irrigações
- **Chave Estrangeira:** id_area em IRRIGACOES

### **7. AREAS_PLANTIO ↔ APLICACOES_NUTRIENTES**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Uma área pode ter várias aplicações
- **Chave Estrangeira:** id_area em APLICACOES_NUTRIENTES

### **8. USUARIOS ↔ IRRIGACOES**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Um usuário pode realizar várias irrigações
- **Chave Estrangeira:** id_usuario em IRRIGACOES

### **9. USUARIOS ↔ APLICACOES_NUTRIENTES**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Um usuário pode realizar várias aplicações
- **Chave Estrangeira:** id_usuario em APLICACOES_NUTRIENTES

### **10. SENSORES ↔ ALERTAS**
- **Relacionamento:** 1:N (Um para Muitos)
- **Cardinalidade:** Um sensor pode gerar vários alertas
- **Chave Estrangeira:** id_sensor em ALERTAS

---

## 📊 **QUERIES DE NEGÓCIO IMPORTANTES**

### **Query 1: Quantidade total de água por mês**
```sql
SELECT 
    DATE_FORMAT(data_hora_inicio, '%Y-%m') as mes,
    SUM(volume_agua_litros) as total_agua_litros
FROM IRRIGACOES 
WHERE data_hora_inicio >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(data_hora_inicio, '%Y-%m')
ORDER BY mes;

### **Query 2: Variação do pH ao longo do ano**
SELECT 
    DATE(ls.data_hora_leitura) as data_leitura,
    AVG(ls.valor) as ph_medio,
    MIN(ls.valor) as ph_minimo,
    MAX(ls.valor) as ph_maximo
FROM LEITURAS_SENSORES ls
JOIN SENSORES s ON ls.id_sensor = s.id_sensor
WHERE s.tipo_sensor = 'PH'
    AND ls.data_hora_leitura >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
GROUP BY DATE(ls.data_hora_leitura)
ORDER BY data_leitura;

### **Query 3: Eficiência por cultura**
SELECT 
    c.nome_cultura,
    COUNT(ap.id_area) as total_areas,
    AVG(ap.area_hectares) as area_media,
    SUM(i.volume_agua_litros) as agua_total
FROM CULTURAS c
JOIN AREAS_PLANTIO ap ON c.id_cultura = ap.id_cultura
LEFT JOIN IRRIGACOES i ON ap.id_area = i.id_area
GROUP BY c.id_cultura, c.nome_cultura;