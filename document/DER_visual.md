# DER Visual - FarmTech Solutions

## 🎨 Diagrama Entidade Relacionamento

![DER FarmTech Solutions](../assets/images/farmtech_der_diagram.png)

## 📋 Descrição do Diagrama

### Entidades Principais (8):
- **FAZENDA** (Azul) - Cadastro das propriedades
- **CULTURA** (Verde) - Plantações e cultivos  
- **SENSOR** (Laranja) - Dispositivos de monitoramento
- **LEITURA_SENSOR** (Roxo) - Dados coletados
- **SISTEMA_IRRIGACAO** (Verde água) - Infraestrutura
- **ACIONAMENTO_IRRIGACAO** (Azul água) - Controle de irrigação
- **INSUMO** (Amarelo) - Produtos agrícolas
- **APLICACAO_INSUMO** (Rosa) - Histórico de aplicações

### Relacionamentos (7):
1. FAZENDA → CULTURA (1:N)
2. CULTURA → SENSOR (1:N)  
3. SENSOR → LEITURA_SENSOR (1:N)
4. CULTURA → SISTEMA_IRRIGACAO (1:N)
5. SISTEMA_IRRIGACAO → ACIONAMENTO_IRRIGACAO (1:N)
6. CULTURA → APLICACAO_INSUMO (1:N)
7. INSUMO → APLICACAO_INSUMO (1:N)

### Características Técnicas:
- **Chaves Primárias:** Destacadas em negrito
- **Chaves Estrangeiras:** Identificadas com (FK)
- **Cardinalidades:** Claramente marcadas (1:N)
- **Tipos de Dados:** Especificados para cada campo
- **Constraints:** NOT NULL, DEFAULT VALUES

## 🛠️ Ferramentas Utilizadas:
- Oracle SQL Developer Data Modeler
- Exportação em alta resolução (300 DPI)
- Formato PNG para compatibilidade universal

*Diagrama criado seguindo padrões de modelagem de dados e boas práticas de design visual.*
