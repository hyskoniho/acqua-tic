#include <OneWire.h>
#include <DallasTemperature.h>
#include "WiFi.h"
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Pinos e definições
#define LDR_PIN 34            // Pino analógico onde o LDR está conectado
#define ONE_WIRE_BUS 4        // Pino digital onde o DS18B20 está conectado
#define HEATER_PIN 12         // Pino digital onde o relé do LED 1 está conectado
#define LAMP_PIN 14          // Pino digital onde o relé do LED 2 está conectado

// Inicializa o barramento OneWire
OneWire oneWire(ONE_WIRE_BUS);

// Inicializa a biblioteca DallasTemperature
DallasTemperature sensors(&oneWire);

// Variáveis de controle (booleanas)
bool heater = true;  // Estado do LED 1 (relé 1)
bool lamp = false;    // Estado do LED 2 (relé 2)

const char* ssid = "Wokwi-GUEST"; // Rede WiFi
const char* password = ""; // Senha
//String* base_url = ";

// Função para enviar os dados via POST para o endpoint "/send-stats"
void sendStats(int lux, float temp) {
  HTTPClient http;
  String url = "https://primary-production-fb02.up.railway.app/webhook/aquatic-data";

  http.begin(url);  // Inicia a conexão HTTP
  http.addHeader("Content-Type", "application/json");  // Define o tipo de conteúdo como JSON

  // Cria o JSON para o POST
  DynamicJsonDocument doc(1024);
  doc["lux"] = lux;
  doc["temp"] = temp;

  String payload;
  serializeJson(doc, payload);  // Serializa o JSON para enviar no corpo da requisição

  int httpCode = http.POST(payload);  // Faz a requisição POST

  if (httpCode > 0) {
    String response = http.getString();
    Serial.println("Resposta do POST: " + response);
  } else {
    Serial.println("Erro na requisição POST");
  }

  http.end();  // Finaliza a conexão
}

// Função para realizar a requisição GET no endpoint "/get-commands" e retornar os valores booleanos
void getCommands(bool &heater, bool &lamp) {
  HTTPClient http;
  String url = "https://primary-production-fb02.up.railway.app/webhook/get-commands";

  http.begin(url);  // Inicia a conexão HTTP
  int httpCode = http.GET();  // Faz a requisição GET

  if (httpCode > 0) {  // Se a requisição foi bem-sucedida
    String payload = http.getString();
    Serial.println("Resposta do GET: " + payload);

    // Parse do JSON de resposta
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);

    heater = doc["heat"];  // Atribui o valor de "heater"
    lamp = doc["lamp"];      // Atribui o valor de "lamp"

    // Exibir os valores de heater e lamp
    Serial.println("Heater: " + String(heater));
    Serial.println("Lamp: " + String(lamp));
  } else {
    Serial.println("Erro na requisição GET");
  }

  http.end();  // Finaliza a conexão
}

void setup() {
  // Configura os pinos dos relés como saída
  pinMode(HEATER_PIN, OUTPUT);
  pinMode(LAMP_PIN, OUTPUT);

  // Configura o pino do LDR como entrada
  pinMode(LDR_PIN, INPUT);

  // Inicializa a comunicação serial
  Serial.begin(115200);

  // Inicializa o sensor de temperatura
  sensors.begin();
  Serial.println("Iniciando leitura do LDR e DS18B20...");

  // Inicializa a conexão à rede WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }

}

void loop() {
  // Leitura do LDR
  int ldrValue = analogRead(LDR_PIN);
  int ldrPercent = map(ldrValue, 0, 4095, 100, 0); // Inverte a escala para porcentagem

  // Exibe o valor do LDR no monitor serial
  Serial.println("Valor LDR (bruto): ");
  Serial.print(ldrValue);
  Serial.print(" | Luz (LDR): ");
  Serial.print(ldrPercent);
  Serial.print(" %");

  // Leitura do sensor de temperatura DS18B20
  sensors.requestTemperatures(); // Solicita a temperatura
  float temperatureC = sensors.getTempCByIndex(0); // Obtém a temperatura em graus Celsius

  // Exibe a temperatura no monitor serial
  if (temperatureC != DEVICE_DISCONNECTED_C) {
    Serial.print(" | Temperatura: ");
    Serial.print(temperatureC);
    Serial.print(" °C");
  } else {
    Serial.println("Sensor de temperatura não conectado!");
  }

  if (WiFi.status() == WL_CONNECTED) {
    // Envia os dados para o servidor
    sendStats(ldrPercent, temperatureC);

    // Recebe os comandos do servidor
    getCommands(heater, lamp);

    // Controla o relé do LED 1
    if (heater) {
      digitalWrite(HEATER_PIN, HIGH);  // Liga o LED 1
      Serial.print("LED 1 (Relé 1) ligado");
    } else {
      digitalWrite(HEATER_PIN, LOW);   // Desliga o LED 1
      Serial.print("LED 1 (Relé 1) desligado");
    }

    // Controla o relé do LED 2
    if (lamp) {
      digitalWrite(LAMP_PIN, HIGH);  // Liga o LED 2
      Serial.print("LED 2 (Relé 2) ligado");
    } else {
      digitalWrite(LAMP_PIN, LOW);   // Desliga o LED 2
      Serial.print("LED 2 (Relé 2) desligado");
    }
  }

  // Aguarda 1 segundo antes de repetir
  delay(1000);
}
