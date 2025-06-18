# FarmTech Solutions - Análise Estatística
# Arquivo: dados_estatisticos.R

# Carregamento de bibliotecas necessárias
if (!require(ggplot2)) install.packages("ggplot2")
if (!require(dplyr)) install.packages("dplyr")
if (!require(readr)) install.packages("readr")

library(ggplot2)
library(dplyr)
library(readr)

# Função para gerar dados simulados das culturas
gerar_dados_simulados <- function() {
  set.seed(123)  # Para reprodutibilidade
  
  # Dados simulados baseados no sistema Python
  dados <- data.frame(
    cultura = c(rep("Café", 10), rep("Milho", 10), rep("Soja", 10)),
    area = c(
      # Café (áreas circulares - variação de raio 15-35m)
      pi * (runif(10, 15, 35))^2,
      # Milho (áreas retangulares - 50-150m x 30-80m)
      runif(10, 50, 150) * runif(10, 30, 80),
      # Soja (áreas retangulares - 60-120m x 40-90m)
      runif(10, 60, 120) * runif(10, 40, 90)
    ),
    producao_estimada = c(
      # Café: 0.8 kg/m²
      pi * (runif(10, 15, 35))^2 * 0.8,
      # Milho: 1.2 kg/m²
      runif(10, 50, 150) * runif(10, 30, 80) * 1.2,
      # Soja: 0.9 kg/m²
      runif(10, 60, 120) * runif(10, 40, 90) * 0.9
    ),
    insumo_necessario = c(
      # Café: 0.5 L/m²
      pi * (runif(10, 15, 35))^2 * 0.5,
      # Milho: 0.3 L/m²
      runif(10, 50, 150) * runif(10, 30, 80) * 0.3,
      # Soja: 0.4 L/m²
      runif(10, 60, 120) * runif(10, 40, 90) * 0.4
    )
  )
  
  return(dados)
}

# Função para calcular estatísticas descritivas
calcular_estatisticas <- function(dados) {
  cat("=== ESTATÍSTICAS DESCRITIVAS - FARMTECH SOLUTIONS ===\n\n")
  
  # Estatísticas por cultura
  stats_por_cultura <- dados %>%
    group_by(cultura) %>%
    summarise(
      n = n(),
      area_media = mean(area),
      area_mediana = median(area),
      area_desvio = sd(area),
      area_min = min(area),
      area_max = max(area),
      producao_media = mean(producao_estimada),
      producao_total = sum(producao_estimada),
      insumo_total = sum(insumo_necessario),
      .groups = 'drop'
    )
  
  print(stats_por_cultura)
  
  # Estatísticas gerais
  cat("\n=== ESTATÍSTICAS GERAIS ===\n")
  cat("Área total cultivada:", sum(dados$area), "m²\n")
  cat("Produção total estimada:", sum(dados$producao_estimada), "kg\n")
  cat("Insumos totais necessários:", sum(dados$insumo_necessario), "L\n")
  cat("Número total de plantações:", nrow(dados), "\n")
  
  return(stats_por_cultura)
}

# Função para gerar gráficos
gerar_graficos <- function(dados) {
  # Gráfico 1: Distribuição de áreas por cultura
  g1 <- ggplot(dados, aes(x = cultura, y = area, fill = cultura)) +
    geom_boxplot() +
    labs(title = "Distribuição de Áreas por Cultura",
         x = "Tipo de Cultura",
         y = "Área (m²)") +
    theme_minimal() +
    scale_fill_manual(values = c("Café" = "#8B4513", 
                                "Milho" = "#FFD700", 
                                "Soja" = "#228B22"))
  
  # Gráfico 2: Produção estimada por cultura
  g2 <- ggplot(dados, aes(x = cultura, y = producao_estimada, fill = cultura)) +
    geom_col() +
    labs(title = "Produção Estimada por Cultura",
         x = "Tipo de Cultura",
         y = "Produção (kg)") +
    theme_minimal() +
    scale_fill_manual(values = c("Café" = "#8B4513", 
                                "Milho" = "#FFD700", 
                                "Soja" = "#228B22"))
  
  # Gráfico 3: Relação área x produção
  g3 <- ggplot(dados, aes(x = area, y = producao_estimada, color = cultura)) +
    geom_point(size = 3) +
    geom_smooth(method = "lm", se = FALSE) +
    labs(title = "Relação entre Área e Produção",
         x = "Área (m²)",
         y = "Produção Estimada (kg)") +
    theme_minimal() +
    scale_color_manual(values = c("Café" = "#8B4513", 
                                 "Milho" = "#FFD700", 
                                 "Soja" = "#228B22"))
  
  # Salvar gráficos
  ggsave("area_por_cultura.png", g1, width = 10, height = 6)
  ggsave("producao_por_cultura.png", g2, width = 10, height = 6)
  ggsave("area_vs_producao.png", g3, width = 10, height = 6)
  
  # Exibir gráficos
  print(g1)
  print(g2)
  print(g3)
}

# Função para análise de correlação
analise_correlacao <- function(dados) {
  cat("\n=== ANÁLISE DE CORRELAÇÃO ===\n")
  
  # Correlação entre área e produção
  cor_area_producao <- cor(dados$area, dados$producao_estimada)
  cat("Correlação Área x Produção:", round(cor_area_producao, 4), "\n")
  
  # Correlação entre área e insumos
  cor_area_insumo <- cor(dados$area, dados$insumo_necessario)
  cat("Correlação Área x Insumos:", round(cor_area_insumo, 4), "\n")
  
  # Correlação entre produção e insumos
  cor_producao_insumo <- cor(dados$producao_estimada, dados$insumo_necessario)
  cat("Correlação Produção x Insumos:", round(cor_producao_insumo, 4), "\n")
}

# Função para teste de hipóteses
teste_hipoteses <- function(dados) {
  cat("\n=== TESTES DE HIPÓTESES ===\n")
  
  # ANOVA para diferenças entre culturas (área)
  anova_area <- aov(area ~ cultura, data = dados)
  cat("ANOVA - Diferenças de área entre culturas:\n")
  print(summary(anova_area))
  
  # ANOVA para diferenças entre culturas (produção)
  anova_producao <- aov(producao_estimada ~ cultura, data = dados)
  cat("\nANOVA - Diferenças de produção entre culturas:\n")
  print(summary(anova_producao))
}

# Função principal
main <- function() {
  cat("🌱 FarmTech Solutions - Análise Estatística em R\n")
  cat("===============================================\n\n")
  
  # Gerar dados
  dados <- gerar_dados_simulados()
  
  # Salvar dados em CSV para integração com Python
  write_csv(dados, "dados_culturas.csv")
  cat("✅ Dados salvos em 'dados_culturas.csv'\n\n")
  
  # Calcular estatísticas
  stats <- calcular_estatisticas(dados)
  
  # Gerar gráficos
  gerar_graficos(dados)
  
  # Análise de correlação
  analise_correlacao(dados)
  
  # Testes de hipóteses
  teste_hipoteses(dados)
  
  cat("\n✅ Análise estatística concluída!")
  cat("\n📊 Gráficos salvos como PNG")
  cat("\n📋 Dados disponíveis em CSV\n")
}

# Executar análise
main()
