#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>
#include <DHT.h>

// Estrutura para armazenar dados dos sensores
struct SensorData {
    float umidade;
    float ph;
    bool fosforo;
    bool potassio;
    unsigned long timestamp;
};

// Classe para gerenciar sensores
class SensorManager {
private:
    DHT* dht_sensor;
    int ldr_pin;
    int fosforo_pin;
    int potassio_pin;
    
public:
    SensorManager(int dht_pin, int ldr_pin, int fosforo_pin, int potassio_pin);
    void init();
    SensorData readAllSensors();
    float readHumidity();
    float readPH();
    bool readPhosphorus();
    bool readPotassium();
};

// Classe para controlar irrigação
class IrrigationController {
private:
    int relay_pin;
    int led_pin;
    bool pump_status;
    
    // Limiares
    float min_humidity;
    float min_ph;
    float max_ph;
    
public:
    IrrigationController(int relay_pin, int led_pin);
    void init();
    void setThresholds(float min_hum, float min_ph, float max_ph);
    bool shouldIrrigate(SensorData data);
    void controlPump(bool state);
    bool getPumpStatus();
};

#endif