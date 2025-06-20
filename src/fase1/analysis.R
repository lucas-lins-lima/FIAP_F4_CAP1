# FarmTech Solutions - Análise Estatística em R
# Fase 1: Análise básica dos dados coletados
# Autor: Equipe FarmTech Solutions
# Data: Dezembro 2024

# Função para instalar e carregar pacotes com tratamento de erro
install_and_load <- function(package_name) {
  if (!require(package_name, character.only = TRUE, quietly = TRUE)) {
    cat("📦 Instalando pacote:", package_name, "\n")
    
    # Tentar diferentes mirrors CRAN
    mirrors <- c(
      "https://cran.rstudio.com/",
      "https://cloud.r-project.org/", 
      "https://cran.r-project.org/"
    )
    
    for (mirror in mirrors) {
      tryCatch({
        options(repos = c(CRAN = mirror))
        install.packages(package_name, dependencies = TRUE, quiet = TRUE)
        break
      }, error = function(e) {
        cat("❌ Erro com mirror", mirror, "\n")
      })
    }
    
    # Tentar carregar novamente
    if (!require(package_name, character.only = TRUE, quietly = TRUE)) {
      cat("❌ Não foi possível instalar/carregar:", package_name, "\n")
      return(FALSE)
    }
  }
  cat("✅ Pacote carregado:", package_name, "\n")
  return(TRUE)
}

# Função para limpar console
clear_console <- function() {
  cat("\014")
}

# Função principal de análise
main_analysis <- function() {
  clear_console()
  
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("🌾 FARMTECH SOLUTIONS - ANÁLISE ESTATÍSTICA EM R 🌾\n")
  cat(paste(rep("=", 60), collapse = ""), "\n")
  cat("Fase 1: Análise de Dados Agrícolas\n")
  cat("FIAP - Faculdade de Informática e Administração Paulista\n")
  cat(paste(rep("=", 60), collapse = ""), "\n\n")
  
  # Instalar e carregar pacotes necessários
  packages <- c("readr", "dplyr", "ggplot2", "knitr")
  packages_loaded <- TRUE
  
  for (pkg in packages) {
    if (!install_and_load(pkg)) {
      packages_loaded <- FALSE
    }
  }
  
  if (!packages_loaded) {
    cat("\n❌ Alguns pacotes não puderam ser carregados.\n")
    cat("💡 Tentando análise básica sem pacotes externos...\n\n")
    basic_analysis()
    return()
  }
  
  cat("\n🔍 Verificando arquivo de dados...\n")
  
  # Verificar se arquivo de dados existe
  data_file <- "data_for_r.csv"
  
  if (!file.exists(data_file)) {
    cat("❌ Arquivo de dados não encontrado:", data_file, "\n")
    cat("🔸 Execute primeiro o sistema Python e:\n")
    cat("   1. Cadastre alguns dados (opção 1 do menu)\n")
    cat("   2. Ou gere dados demo (opção 6 do menu)\n")
    cat("   3. Visualize os dados (opção 2) para exportar CSV\n\n")
    
    # Criar dados exemplo se não existir
    create_example_data()
    return()
  }
  
  # Carregar dados
  tryCatch({
    dados <- read.csv(data_file, stringsAsFactors = FALSE, encoding = "UTF-8")
    cat("✅ Dados carregados com sucesso!\n")
    cat("📊 Total de registros:", nrow(dados), "\n\n")
  }, error = function(e) {
    cat("❌ Erro ao carregar dados:", e$message, "\n")
    cat("💡 Tentando análise básica...\n\n")
    basic_analysis()
    return()
  })
  
  # Verificar se há dados
  if (nrow(dados) == 0) {
    cat("❌ Nenhum dado encontrado no arquivo.\n")
    return()
  }
  
  # Análises estatísticas
  perform_statistical_analysis(dados)
  
  # Gerar gráficos (se ggplot2 estiver disponível)
  if (require("ggplot2", quietly = TRUE)) {
    generate_plots(dados)
  }
  
  # Salvar relatório
  save_report(dados)
  
  cat("\n✅ Análise concluída com sucesso!\n")
  cat("📄 Relatório salvo em: relatorio_estatistico.txt\n")
}

# Análise básica sem pacotes externos
basic_analysis <- function() {
  cat("📈 ANÁLISE BÁSICA (sem pacotes externos)\n")
  cat(paste(rep("-", 40), collapse = ""), "\n")
  
  # Criar dados exemplo simples
  areas <- c(60000, 70686, 43000, 60000)
  culturas <- c("Soja", "Milho", "Café", "Cana-de-açúcar")
  
  cat("\n🌾 ESTATÍSTICAS BÁSICAS DAS ÁREAS (m²):\n")
  cat("Média:", round(mean(areas), 2), "\n")
  cat("Mediana:", round(median(areas), 2), "\n")
  cat("Desvio Padrão:", round(sd(areas), 2), "\n")
  cat("Mínimo:", min(areas), "\n")
  cat("Máximo:", max(areas), "\n")
  
  cat("\n🌱 CULTURAS EXEMPLO:\n")
  for (i in 1:length(culturas)) {
    cat(culturas[i], ":", areas[i], "m²\n")
  }
  
  cat("\n💡 Para análise completa, instale os pacotes: readr, dplyr, ggplot2, knitr\n")
}

# Criar dados exemplo se não existir arquivo
create_example_data <- function() {
  cat("📝 Criando arquivo de exemplo...\n")
  
  exemplo_data <- data.frame(
    id = 1:4,
    nome_area = c("Fazenda São João - Lote A", "Propriedade Rural Esperança", 
                  "Cafezal Monte Verde", "Usina Doce Vida - Setor B"),
    cultura = c("Soja", "Milho", "Café", "Cana-de-açúcar"),
    area = c(60000, 70686, 43000, 60000),
    insumo_nome = c("Glifosato", "Ureia", "Fosfato", "NPK Líquido"),
    insumo_quantidade = c(18.0, 1413.72, 645.0, 30000.0),
    insumo_unidade = c("L", "kg", "kg", "mL"),
    timestamp = rep(Sys.time(), 4)
  )
  
  write.csv(exemplo_data, "data_for_r.csv", row.names = FALSE)
  cat("✅ Arquivo de exemplo criado: data_for_r.csv\n")
  cat("🔄 Execute o script novamente para análise completa.\n")
}

# Análise estatística detalhada
perform_statistical_analysis <- function(dados) {
  cat("📈 ANÁLISE ESTATÍSTICA DETALHADA\n")
  cat(paste(rep("-", 40), collapse = ""), "\n")
  
  # Estatísticas descritivas das áreas
  cat("\n🌾 ESTATÍSTICAS DAS ÁREAS (m²):\n")
  
  area_stats <- data.frame(
    Métrica = c("Média", "Mediana", "Desvio Padrão", "Mínimo", "Máximo", "Variância"),
    Valor = c(
      round(mean(dados$area, na.rm = TRUE), 2),
      round(median(dados$area, na.rm = TRUE), 2),
      round(sd(dados$area, na.rm = TRUE), 2),
      round(min(dados$area, na.rm = TRUE), 2),
      round(max(dados$area, na.rm = TRUE), 2),
      round(var(dados$area, na.rm = TRUE), 2)
    )
  )
  
  print(area_stats)
  
  # Distribuição por cultura
  cat("\n🌱 DISTRIBUIÇÃO POR CULTURA:\n")
  cultura_summary <- aggregate(dados$area, by = list(dados$cultura), 
                              FUN = function(x) c(Quantidade = length(x), 
                                                 Area_Total = sum(x),
                                                 Area_Media = mean(x)))
  
  for (i in 1:nrow(cultura_summary)) {
    cat(cultura_summary[i,1], ":\n")
    cat("  Quantidade:", cultura_summary[i,2][1], "registro(s)\n")
    cat("  Área Total:", round(cultura_summary[i,2][2], 2), "m²\n")
    cat("  Área Média:", round(cultura_summary[i,2][3], 2), "m²\n\n")
  }
  
  # Análise de insumos
  cat("🧪 ANÁLISE DE INSUMOS:\n")
  insumo_summary <- aggregate(dados$insumo_quantidade, 
                             by = list(dados$insumo_nome, dados$insumo_unidade),
                             FUN = function(x) c(Total = sum(x), Media = mean(x), DP = sd(x)))
  
  for (i in 1:nrow(insumo_summary)) {
    cat(insumo_summary[i,1], "(", insumo_summary[i,2], "):\n")
    cat("  Total:", round(insumo_summary[i,3][1], 2), "\n")
    cat("  Média:", round(insumo_summary[i,3][2], 2), "\n")
    cat("  Desvio Padrão:", round(insumo_summary[i,3][3], 2), "\n\n")
  }
  
  # Correlações
  if (nrow(dados) > 2) {
    cat("📊 CORRELAÇÃO ÁREA vs QUANTIDADE DE INSUMO:\n")
    correlacao <- cor(dados$area, dados$insumo_quantidade, use = "complete.obs")
    cat("Correlação de Pearson:", round(correlacao, 4), "\n")
    
    if (abs(correlacao) > 0.7) {
      cat("✅ Correlação forte detectada!\n")
    } else if (abs(correlacao) > 0.3) {
      cat("🔸 Correlação moderada detectada.\n")
    } else {
      cat("❌ Correlação fraca.\n")
    }
  }
}

# Geração de gráficos
generate_plots <- function(dados) {
  cat("\n📊 GERANDO GRÁFICOS...\n")
  
  # Criar diretório para gráficos se não existir
  if (!dir.exists("graficos")) {
    dir.create("graficos")
  }
  
  tryCatch({
    # Gráfico 1: Distribuição das áreas por cultura
    p1 <- ggplot(dados, aes(x = cultura, y = area, fill = cultura)) +
      geom_boxplot(alpha = 0.7) +
      geom_jitter(width = 0.2, alpha = 0.6) +
      labs(
        title = "Distribuição das Áreas por Cultura",
        subtitle = "FarmTech Solutions - Análise Fase 1",
        x = "Cultura",
        y = "Área (m²)",
        fill = "Cultura"
      ) +
      theme_minimal() +
      theme(
        plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x = element_text(angle = 45, hjust = 1)
      )
    
    ggsave("graficos/distribuicao_areas_cultura.png", p1, width = 10, height = 6, dpi = 300)
    
    # Gráfico 2: Quantidade de insumos
    p2 <- ggplot(dados, aes(x = insumo_nome, y = insumo_quantidade, fill = insumo_nome)) +
      geom_col(alpha = 0.8) +
      labs(
        title = "Quantidade Total de Insumos por Tipo",
        subtitle = "FarmTech Solutions - Análise Fase 1",
        x = "Tipo de Insumo",
        y = "Quantidade Total",
        fill = "Insumo"
      ) +
      theme_minimal() +
      theme(
        plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
        plot.subtitle = element_text(hjust = 0.5),
        axis.text.x = element_text(angle = 45, hjust = 1)
      )
    
    ggsave("graficos/quantidade_insumos.png", p2, width = 10, height = 6, dpi = 300)
    
    cat("✅ Gráficos salvos na pasta 'graficos/'\n")
    
  }, error = function(e) {
    cat("❌ Erro ao gerar gráficos:", e$message, "\n")
  })
}

# Salvar relatório completo
save_report <- function(dados) {
  # Criar arquivo de relatório
  report_file <- "relatorio_estatistico.txt"
  
  # Gerar timestamp
  timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  
  # Escrever relatório
  cat(paste(rep("=", 60), collapse = ""), "\n", file = report_file)
  cat("FARMTECH SOLUTIONS - RELATÓRIO ESTATÍSTICO\n", file = report_file, append = TRUE)
  cat(paste(rep("=", 60), collapse = ""), "\n", file = report_file, append = TRUE)
  cat("Data da análise:", timestamp, "\n", file = report_file, append = TRUE)
  cat("Total de registros analisados:", nrow(dados), "\n\n", file = report_file, append = TRUE)
  
  # Estatísticas básicas
  cat("ESTATÍSTICAS DAS ÁREAS:\n", file = report_file, append = TRUE)
  cat("Área média:", round(mean(dados$area), 2), "m²\n", file = report_file, append = TRUE)
  cat("Desvio padrão:", round(sd(dados$area), 2), "m²\n", file = report_file, append = TRUE)
  cat("Área total:", round(sum(dados$area), 2), "m²\n", file = report_file, append = TRUE)
  
  # Distribuição por cultura
  cat("\nDISTRIBUIÇÃO POR CULTURA:\n", file = report_file, append = TRUE)
  culturas_unicas <- unique(dados$cultura)
  
  for (cultura in culturas_unicas) {
    cultura_dados <- subset(dados, cultura == cultura)
    cat(cultura, ":", nrow(cultura_dados), 
        "registros (", round(sum(cultura_dados$area), 2), "m²)\n", 
        file = report_file, append = TRUE)
  }
  
  cat("\n\n", file = report_file, append = TRUE)
  cat("Análise gerada automaticamente pelo sistema FarmTech Solutions\n", 
      file = report_file, append = TRUE)
  cat("FIAP - Fase 1 do Projeto\n", file = report_file, append = TRUE)
}

# Executar análise principal
main_analysis()