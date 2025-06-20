#ifndef LCD_DISPLAY_H
#define LCD_DISPLAY_H

#include <LiquidCrystal_I2C.h>
#include <Arduino.h>

// Classe otimizada para gerenciar o display LCD
class OptimizedLCDManager {
private:
    LiquidCrystal_I2C* lcd;
    uint8_t current_screen;
    uint32_t last_update;
    uint16_t update_interval;
    
    // Caracteres customizados
    uint8_t char_humidity[8] = {0x04, 0x0E, 0x0E, 0x1F, 0x1F, 0x1F, 0x0E, 0x00};
    uint8_t char_ph[8] = {0x0E, 0x11, 0x11, 0x0E, 0x04, 0x04, 0x04, 0x00};
    uint8_t char_nutrient[8] = {0x0A, 0x0A, 0x1F, 0x11, 0x0A, 0x04, 0x0A, 0x00};
    uint8_t char_pump[8] = {0x04, 0x0E, 0x1F, 0x1F, 0x1F, 0x0E, 0x04, 0x00};
    
public:
    // Construtor otimizado
    OptimizedLCDManager(uint8_t address = 0x27, uint8_t cols = 20, uint8_t rows = 4) 
        : current_screen(0), last_update(0), update_interval(2000) {
        lcd = new LiquidCrystal_I2C(address, cols, rows);
    }
    
    // Inicialização
    void init() {
        lcd->init();
        lcd->backlight();
        
        // Criar caracteres customizados
        lcd->createChar(0, char_humidity);
        lcd->createChar(1, char_ph);
        lcd->createChar(2, char_nutrient);
        lcd->createChar(3, char_pump);
        
        showStartupScreen();
    }
    
    // Tela de inicialização
    void showStartupScreen() {
        lcd->clear();
        lcd->setCursor(2, 0);
        lcd->print(F("FarmTech Solutions"));
        lcd->setCursor(6, 1);
        lcd->print(F("v4.0 Pro"));
        lcd->setCursor(4, 2);
        lcd->print(F("Sistema Otimizado"));
        lcd->setCursor(7, 3);
        lcd->print(F("Carregando..."));
    }
    
    // Atualização inteligente do display
    bool shouldUpdate() {
        return (millis() - last_update) >= update_interval;
    }
    
    // Exibir dados dos sensores
    void displaySensorData(float humidity, float ph, bool phosphorus, bool potassium, bool pump_active) {
        if (!shouldUpdate()) return;
        
        lcd->clear();
        
        switch (current_screen) {
            case 0: // Tela principal
                lcd->setCursor(0, 0);
                lcd->print(F("FarmTech Pro v4.0"));
                
                lcd->setCursor(0, 1);
                lcd->write(0); // Ícone umidade
                lcd->print(F(" Umidade: "));
                lcd->print(humidity, 1);
                lcd->print(F("%"));
                
                lcd->setCursor(0, 2);
                lcd->write(1); // Ícone pH
                lcd->print(F(" pH: "));
                lcd->print(ph, 2);
                
                lcd->setCursor(12, 2);
                lcd->write(3); // Ícone bomba
                lcd->print(pump_active ? F(" ON") : F("OFF"));
                
                lcd->setCursor(0, 3);
                lcd->print(F("Status: "));
                if (humidity > 40 && ph >= 6.0 && ph <= 7.5) {
                    lcd->print(F("IDEAL"));
                } else {
                    lcd->print(F("ATENCAO"));
                }
                break;
                
            case 1: // Tela de nutrientes
                lcd->setCursor(0, 0);
                lcd->print(F("ANALISE NUTRIENTES"));
                
                lcd->setCursor(0, 1);
                lcd->write(2);
                lcd->print(F(" Fosforo (P):"));
                lcd->setCursor(15, 1);
                lcd->print(phosphorus ? F("OK") : F("BAIXO"));
                
                lcd->setCursor(0, 2);
                lcd->write(2);
                lcd->print(F(" Potassio (K):"));
                lcd->setCursor(15, 2);
                lcd->print(potassium ? F("OK") : F("BAIXO"));
                
                lcd->setCursor(0, 3);
                lcd->print(F("Fertilizar: "));
                lcd->print((!phosphorus || !potassium) ? F("SIM") : F("NAO"));
                break;
                
            case 2: // Tela de sistema
                lcd->setCursor(0, 0);
                lcd->print(F("INFO DO SISTEMA"));
                
                lcd->setCursor(0, 1);
                lcd->print(F("Uptime: "));
                lcd->print(millis() / 1000);
                lcd->print(F("s"));
                
                lcd->setCursor(0, 2);
                lcd->print(F("Memoria: "));
                lcd->print(ESP.getFreeHeap() / 1024);
                lcd->print(F("KB"));
                
                lcd->setCursor(0, 3);
                lcd->print(F("CPU: "));
                lcd->print(ESP.getCpuFreqMHz());
                lcd->print(F("MHz"));
                break;
        }
        
        // Alternar tela
        current_screen = (current_screen + 1) % 3;
        last_update = millis();
    }
    
    // Exibir mensagem de erro
    void displayError(const char* error_msg) {
        lcd->clear();
        lcd->setCursor(0, 0);
        lcd->print(F("ERRO DO SISTEMA"));
        lcd->setCursor(0, 2);
        lcd->print(error_msg);
    }
    
    // Destrutor
    ~OptimizedLCDManager() {
        delete lcd;
    }
};

#endif