#include <DHT.h>
// Removido WiFi.h para compatibilidade
// Removido LiquidCrystal_I2C.h (não disponível no Wokwi gratuito)

// ==================== OTIMIZAÇÕES DE MEMÓRIA ====================
// Usando tipos de dados otimizados para economizar memória
// uint8_t ao invés de int (8 bits ao invés de 32)
// float ao invés de double (32 bits ao invés de 64)

// Definições dos pinos - usando constexpr para otimização
constexpr uint8_t DHT_PIN = 4;
constexpr uint8_t LDR_PIN = 34;
constexpr uint8_t FOSFORO_BTN = 18;
constexpr uint8_t POTASSIO_BTN = 19;
constexpr uint8_t RELE_PIN = 2;
// REMOVIDO: LED_BUILTIN redefinition - usar o padrão do ESP32

// Configurações do DHT22
constexpr uint8_t DHT_TYPE = DHT22;
DHT dht(DHT_PIN, DHT_TYPE);

// ==================== ESTRUTURAS OTIMIZADAS ====================
struct SensorData {
  float humidity;      // 4 bytes
  float ph_value;      // 4 bytes
  bool phosphorus;     // 1 byte
  bool potassium;      // 1 byte
  bool pump_active;    // 1 byte
  uint32_t timestamp;  // 4 bytes
} __attribute__((packed)); // Compactar estrutura para economizar memória

// ==================== VARIÁVEIS GLOBAIS OTIMIZADAS ====================
SensorData current_data = {0.0f, 0.0f, false, false, false, 0};

// Limiares como constantes para economizar RAM
constexpr float HUMIDITY_MIN = 30.0f;
constexpr float PH_MIN = 6.0f;
constexpr float PH_MAX = 7.5f;

// Controle de timing otimizado
uint32_t last_reading = 0;
uint32_t last_serial_output = 0;
constexpr uint16_t READING_INTERVAL = 5000;   // 5 segundos
constexpr uint16_t SERIAL_INTERVAL = 2000;    // 2 segundos para Serial Plotter

// Contador para saída alternada
bool detailed_output = false;

// ==================== SETUP OTIMIZADO ====================
void setup() {
  Serial.begin(115200);
  
  // Configuração dos pinos de forma otimizada
  const uint8_t input_pins[] = {FOSFORO_BTN, POTASSIO_BTN};
  const uint8_t output_pins[] = {RELE_PIN, LED_BUILTIN};
  
  for (uint8_t pin : input_pins) {
    pinMode(pin, INPUT_PULLUP);
  }
  
  for (uint8_t pin : output_pins) {
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
  }
  
  // Inicialização do DHT22
  dht.begin();
  
  // Mensagens de inicialização otimizadas (usando F() para PROGMEM)
  Serial.println(F("=== FARMTECH SOLUTIONS v4.0 ==="));
  Serial.println(F("Sistema Otimizado - Wokwi Compatible"));
  Serial.println(F("Recursos: Serial Plotter, Otimizado"));
  Serial.println(F("================================"));
  Serial.println(F(""));
  Serial.println(F("Legenda Serial Plotter:"));
  Serial.println(F("- Humidity: Umidade do solo (%)"));
  Serial.println(F("- pH: Nivel de pH * 10"));
  Serial.println(F("- Pump: Status bomba (0=OFF, 100=ON)"));
  Serial.println(F("- Phosphorus: Fosforo * 20 (0=Ausente, 20=Presente)"));
  Serial.println(F("- Potassium: Potassio * 30 (0=Ausente, 30=Presente)"));
  Serial.println(F("================================"));
  
  delay(3000);
  Serial.println(F("Sistema iniciado! Dados a cada 5s..."));
}

// ==================== FUNÇÕES OTIMIZADAS ====================

// Leitura otimizada dos sensores
inline void readSensorsOptimized() {
  // Leitura do DHT22 com verificação de erro
  float h = dht.readHumidity();
  if (!isnan(h)) {
    current_data.humidity = h;
  }
  
  // Leitura do LDR para pH (otimizada)
  uint16_t ldr_raw = analogRead(LDR_PIN);
  current_data.ph_value = map(ldr_raw, 0, 4095, 0, 1400) * 0.01f; // Conversão otimizada
  
  // Leitura dos botões (invertida devido ao pullup)
  current_data.phosphorus = !digitalRead(FOSFORO_BTN);
  current_data.potassium = !digitalRead(POTASSIO_BTN);
  
  // Timestamp otimizado
  current_data.timestamp = millis();
}

// Lógica de irrigação otimizada
bool shouldIrrigate() {
  return (current_data.humidity < HUMIDITY_MIN) ||
         (current_data.ph_value < PH_MIN || current_data.ph_value > PH_MAX) ||
         (!current_data.phosphorus || !current_data.potassium);
}

void controlIrrigation() {
  static bool previous_state = false;
  bool should_pump = shouldIrrigate();
  
  if (should_pump != previous_state) {
    current_data.pump_active = should_pump;
    digitalWrite(RELE_PIN, should_pump ? HIGH : LOW);
    digitalWrite(LED_BUILTIN, should_pump ? HIGH : LOW);
    
    // Log apenas quando houver mudança de estado
    Serial.print(F("PUMP STATUS CHANGE: "));
    Serial.println(should_pump ? F("ON") : F("OFF"));
    
    previous_state = should_pump;
  }
}

// Saída otimizada para Serial Plotter
void printSerialPlotterData() {
  // Formato específico para Serial Plotter do Wokwi
  Serial.print(F("Humidity:"));
  Serial.print(current_data.humidity, 1);
  Serial.print(F(",pH:"));
  Serial.print(current_data.ph_value * 10, 1); // Multiplicar por 10 para melhor visualização
  Serial.print(F(",Pump:"));
  Serial.print(current_data.pump_active ? 100 : 0);
  Serial.print(F(",Phosphorus:"));
  Serial.print(current_data.phosphorus ? 20 : 0);
  Serial.print(F(",Potassium:"));
  Serial.println(current_data.potassium ? 30 : 0);
}

// Saída detalhada para monitoramento
void printDetailedData() {
  Serial.println(F("--- LEITURA DE SENSORES ---"));
  Serial.print(F("Timestamp: ")); Serial.println(current_data.timestamp);
  Serial.print(F("Umidade: ")); Serial.print(current_data.humidity, 1); Serial.println(F("%"));
  Serial.print(F("pH: ")); Serial.println(current_data.ph_value, 2);
  Serial.print(F("Fosforo: ")); Serial.println(current_data.phosphorus ? F("PRESENTE") : F("AUSENTE"));
  Serial.print(F("Potassio: ")); Serial.println(current_data.potassium ? F("PRESENTE") : F("AUSENTE"));
  Serial.print(F("Bomba: ")); Serial.println(current_data.pump_active ? F("ATIVA") : F("INATIVA"));
  Serial.print(F("Memoria livre: ")); Serial.print(ESP.getFreeHeap()); Serial.println(F(" bytes"));
  
  // Dados CSV para coleta manual
  Serial.print(F("CSV: "));
  Serial.print(current_data.timestamp);
  Serial.print(F(","));
  Serial.print(current_data.humidity, 2);
  Serial.print(F(","));
  Serial.print(current_data.ph_value, 2);
  Serial.print(F(","));
  Serial.print(current_data.phosphorus ? 1 : 0);
  Serial.print(F(","));
  Serial.print(current_data.potassium ? 1 : 0);
  Serial.print(F(","));
  Serial.println(current_data.pump_active ? 1 : 0);
  
  Serial.println(F("---------------------------"));
}

// Função para mostrar estatísticas de otimização
void printOptimizationStats() {
  Serial.println(F("=== ESTATISTICAS DE OTIMIZACAO ==="));
  Serial.print(F("Tamanho da estrutura SensorData: "));
  Serial.print(sizeof(SensorData));
  Serial.println(F(" bytes"));
  
  Serial.print(F("Memoria heap livre: "));
  Serial.print(ESP.getFreeHeap());
  Serial.println(F(" bytes"));
  
  Serial.print(F("Frequencia da CPU: "));
  Serial.print(ESP.getCpuFreqMHz());
  Serial.println(F(" MHz"));
  
  Serial.print(F("Uptime: "));
  Serial.print(millis() / 1000);
  Serial.println(F(" segundos"));
  Serial.println(F("=================================="));
}

// ==================== LOOP PRINCIPAL OTIMIZADO ====================
void loop() {
  uint32_t current_time = millis();
  
  // Leitura dos sensores em intervalo otimizado
  if (current_time - last_reading >= READING_INTERVAL) {
    readSensorsOptimized();
    controlIrrigation();
    last_reading = current_time;
  }
  
  // Saída serial em intervalo diferente para otimização
  if (current_time - last_serial_output >= SERIAL_INTERVAL) {
    // Alternar entre saída detalhada e Serial Plotter
    if (detailed_output) {
      printDetailedData();
      
      // Mostrar estatísticas a cada 30 segundos
      static uint32_t last_stats = 0;
      if (current_time - last_stats >= 30000) {
        printOptimizationStats();
        last_stats = current_time;
      }
    } else {
      printSerialPlotterData();
    }
    
    detailed_output = !detailed_output;
    last_serial_output = current_time;
  }
  
  // Pequeno delay para economizar CPU
  delay(50); // Reduzido para melhor responsividade
}