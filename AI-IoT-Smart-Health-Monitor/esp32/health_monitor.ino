/*
 * AI-Driven IoT Smart Health Monitoring System
 * ESP32 Firmware — Reads MAX30102 + DS18B20 sensors
 * and sends data to Firebase via WiFi
 *
 * Author : Sam Wesley S
 * College : Karunya Institute of Technology and Sciences
 *
 * Required Libraries (install via Arduino Library Manager):
 *   - FirebaseESP32 by Mobizt
 *   - MAX30105 by SparkFun
 *   - DallasTemperature by Miles Burton
 *   - OneWire by Paul Stoffregen
 */

#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Wire.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include <OneWire.h>
#include <DallasTemperature.h>

// ── WiFi Credentials ───────────────────────────────────────────────────────────
#define WIFI_SSID     "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ── Firebase Credentials ───────────────────────────────────────────────────────
#define FIREBASE_HOST "your-project.firebaseio.com"
#define FIREBASE_AUTH "your-firebase-auth-token"

// ── Sensor Pins ────────────────────────────────────────────────────────────────
#define DS18B20_PIN 4    // DS18B20 data pin

// ── Objects ────────────────────────────────────────────────────────────────────
FirebaseData   fbData;
FirebaseConfig fbConfig;
FirebaseAuth   fbAuth;
MAX30105       particleSensor;
OneWire        oneWire(DS18B20_PIN);
DallasTemperature tempSensor(&oneWire);

// ── Buffers for SpO2 calculation ───────────────────────────────────────────────
#define BUFFER_SIZE 100
uint32_t irBuffer[BUFFER_SIZE];
uint32_t redBuffer[BUFFER_SIZE];
int32_t  spo2, heartRate;
int8_t   validSPO2, validHeartRate;

void setup() {
  Serial.begin(115200);

  // WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());

  // Firebase
  fbConfig.host = FIREBASE_HOST;
  fbConfig.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&fbConfig, &fbAuth);
  Firebase.reconnectWiFi(true);

  // MAX30102
  Wire.begin();
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found!");
    while (1);
  }
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeIR(0x1F);

  // DS18B20
  tempSensor.begin();

  Serial.println("Health Monitor Ready!");
}

void loop() {
  // ── Read SpO2 + Heart Rate ─────────────────────────────────────────────────
  for (int i = 0; i < BUFFER_SIZE; i++) {
    while (!particleSensor.available())
      particleSensor.check();
    redBuffer[i] = particleSensor.getRed();
    irBuffer[i]  = particleSensor.getIR();
    particleSensor.nextSample();
  }
  maxim_heart_rate_and_oxygen_saturation(
    irBuffer, BUFFER_SIZE, redBuffer,
    &spo2, &validSPO2, &heartRate, &validHeartRate);

  // ── Read Temperature ───────────────────────────────────────────────────────
  tempSensor.requestTemperatures();
  float temperature = tempSensor.getTempCByIndex(0);

  // ── Validate and print ─────────────────────────────────────────────────────
  int hr_val   = (validHeartRate && heartRate > 0 && heartRate < 200) ? heartRate : 0;
  int spo2_val = (validSPO2 && spo2 > 0 && spo2 <= 100)              ? spo2      : 0;

  Serial.printf("HR: %d BPM | SpO2: %d%% | Temp: %.1f°C\n",
                hr_val, spo2_val, temperature);

  // ── Push to Firebase ───────────────────────────────────────────────────────
  if (Firebase.ready()) {
    FirebaseJson json;
    json.set("heart_rate",  hr_val);
    json.set("spo2",        spo2_val);
    json.set("temperature", temperature);
    json.set("timestamp",   String(millis()));

    if (Firebase.setJSON(fbData, "/vitals/latest", json)) {
      Serial.println("Firebase: Data pushed.");
    } else {
      Serial.println("Firebase Error: " + fbData.errorReason());
    }

    // Also push to history
    Firebase.pushJSON(fbData, "/vitals/history", json);
  }

  delay(5000);   // Send every 5 seconds
}
