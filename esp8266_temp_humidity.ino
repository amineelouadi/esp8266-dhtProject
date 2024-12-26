#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// WiFi Configuration
const char* ssid = "Fibre_MarocTelecom_2.4G";
const char* password = "6RzGKSHf";

// API Configuration
const char* apiEndpoint = "http://192.168.1.168:8000/api/sensor-data/";
const char* deviceId = "esp8266-001";

// DHT Sensor Configuration
#define DHTPIN 2       // GPIO2/D4 on ESP8266
#define DHTTYPE DHT11  // DHT11 sensor type
DHT dht(DHTPIN, DHTTYPE);

// Timing Configuration
const unsigned long READING_INTERVAL = 30000;  // 30 seconds
unsigned long lastReadingTime = 0;

void setup() {
    // Initialize Serial communication
    Serial.begin(115200);
    Serial.println("\nESP8266 Temperature & Humidity Sensor");
    
    // Initialize DHT sensor
    dht.begin();
    
    // Connect to WiFi
    connectToWiFi();
}

void loop() {
    // Check WiFi connection
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi connection lost. Reconnecting...");
        connectToWiFi();
    }
    
    // Check if it's time to take a new reading
    unsigned long currentTime = millis();
    if (currentTime - lastReadingTime >= READING_INTERVAL) {
        // Read sensor data
        float humidity = dht.readHumidity();
        float temperature = dht.readTemperature();
        
        // Check if readings are valid
        if (isnan(humidity) || isnan(temperature)) {
            Serial.println("Failed to read from DHT sensor!");
        } else {
            // Print readings to Serial Monitor
            Serial.print("Temperature: ");
            Serial.print(temperature);
            Serial.print("°C, Humidity: ");
            Serial.print(humidity);
            Serial.println("%");
            
            // Send data to API
            sendSensorData(temperature, humidity);
        }
        
        lastReadingTime = currentTime;
    }
}

void connectToWiFi() {
    Serial.print("Connecting to WiFi");
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nConnected to WiFi");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void sendSensorData(float temperature, float humidity) {
    WiFiClient client;
    HTTPClient http;
    
    // Create JSON payload
    StaticJsonDocument<200> doc;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["device"] = deviceId;
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    // Send HTTP POST request
    http.begin(client, apiEndpoint);
    http.addHeader("Content-Type", "application/json");
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String response = http.getString();
        Serial.println("Response:");
        Serial.println(response);
    } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
    }
    
    http.end();
}