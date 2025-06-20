#include <WiFi.h>
#include <DHT.h>

// Definições dos pinos
#define DHT_PIN 4
#define LDR_PIN 34
#define FOSFORO_BTN 18
#define POTASSIO_BTN 19
#define RELE_PIN 2
#define LED_BUILTIN 23

// Configurações do DHT22
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

// Variáveis globais
float umidade = 0.0;
float ph_valor = 0.0;
bool fosforo_presente = false;
bool potassio_presente = false;
bool bomba_ativa = false;

// Limiares para irrigação
const float UMIDADE_MIN = 30.0;  // 30% mínimo de umidade
const float PH_MIN = 6.0;        // pH mínimo
const float PH_MAX = 7.5;        // pH máximo

// Configuração inicial
void setup() {
  Serial.begin(115200);
  
  // Inicialização dos pinos
  pinMode(FOSFORO_BTN, INPUT_PULLUP);
  pinMode(POTASSIO_BTN, INPUT_PULLUP);
  pinMode(RELE_PIN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // Inicialização do sensor DHT
  dht.begin();
  
  // Estado inicial da bomba (desligada)
  digitalWrite(RELE_PIN, LOW);
  digitalWrite(LED_BUILTIN, LOW);
  bomba_ativa = false;
  
  Serial.println("=== SISTEMA FARMTECH SOLUTIONS ===");
  Serial.println("Sistema de Irrigação Inteligente Iniciado");
  Serial.println("Sensores: Umidade, pH, Fósforo, Potássio");
  Serial.println("=====================================");
  delay(2000);
}

// Função para ler sensores
void lerSensores() {
  // Leitura do sensor de umidade (DHT22)
  umidade = dht.readHumidity();
  
  // Leitura do sensor de pH (simulado com LDR)
  int ldr_valor = analogRead(LDR_PIN);
  // Conversão do valor LDR (0-4095) para pH (0-14)
  ph_valor = map(ldr_valor, 0, 4095, 0, 1400) / 100.0;
  
  // Leitura dos sensores de nutrientes (botões)
  fosforo_presente = !digitalRead(FOSFORO_BTN);  // Invertido (pullup)
  potassio_presente = !digitalRead(POTASSIO_BTN); // Invertido (pullup)
}

// Lógica de controle da irrigação
void controlarIrrigacao() {
  bool deve_irrigar = false;
  String motivo = "";
  
  // Verificação das condições para irrigação
  if (umidade < UMIDADE_MIN) {
    deve_irrigar = true;
    motivo += "Umidade baixa (" + String(umidade) + "%) ";
  }
  
  if (ph_valor < PH_MIN || ph_valor > PH_MAX) {
    deve_irrigar = true;
    motivo += "pH inadequado (" + String(ph_valor) + ") ";
  }
  
  if (!fosforo_presente || !potassio_presente) {
    deve_irrigar = true;
    motivo += "Nutrientes insuficientes ";
  }
  
  // Controle da bomba
  if (deve_irrigar && !bomba_ativa) {
    // Ligar bomba
    digitalWrite(RELE_PIN, HIGH);
    digitalWrite(LED_BUILTIN, HIGH);
    bomba_ativa = true;
    Serial.println("🔴 BOMBA LIGADA - Motivo: " + motivo);
  } 
  else if (!deve_irrigar && bomba_ativa) {
    // Desligar bomba
    digitalWrite(RELE_PIN, LOW);
    digitalWrite(LED_BUILTIN, LOW);
    bomba_ativa = false;
    Serial.println("🟢 BOMBA DESLIGADA - Condições adequadas");
  }
}

// Função para exibir dados no monitor serial
void exibirDados() {
  Serial.println("--- LEITURA DE SENSORES ---");
  Serial.printf("Umidade: %.2f%%\n", umidade);
  Serial.printf("pH: %.2f\n", ph_valor);
  Serial.printf("Fósforo: %s\n", fosforo_presente ? "PRESENTE" : "AUSENTE");
  Serial.printf("Potássio: %s\n", potassio_presente ? "PRESENTE" : "AUSENTE");
  Serial.printf("Bomba: %s\n", bomba_ativa ? "LIGADA" : "DESLIGADA");
  Serial.println("---------------------------");
  
  // Dados formatados para coleta (CSV)
  Serial.printf("DATA,%lu,%.2f,%.2f,%d,%d,%d\n", 
                millis(), umidade, ph_valor, 
                fosforo_presente, potassio_presente, bomba_ativa);
}

// Loop principal
void loop() {
  // Leitura dos sensores
  lerSensores();
  
  // Controle da irrigação
  controlarIrrigacao();
  
  // Exibição dos dados
  exibirDados();
  
  // Aguarda 5 segundos antes da próxima leitura
  delay(5000);
}