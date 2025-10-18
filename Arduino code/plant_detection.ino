/*
 * Smart Plant Incubator System with Automatic Watering and Lighting
 * File: plant_incubator.c
 * 
 * Hardware:
 * - Arduino UNO connected to Raspberry Pi via USB
 * - DHT22 Temperature/Humidity Sensor (Pin 2)
 * - Soil Moisture Sensor (Analog Pin A0)
 * - LDR Light Sensor (Analog Pin A1)
 * - Water Pump Relay (Pin 8 - Active LOW)
 * - Incubator Lights Relay (Pin 9 - Active LOW)
 */

#include <DHT.h>
 
// Pin definitions
#define DHTPIN 2           // DHT sensor data pin
#define DHTTYPE DHT22      // DHT22 sensor type
#define SOIL_MOISTURE_PIN A0
#define LDR_PIN A1
#define PUMP_RELAY_PIN 8   // Active LOW relay for water pump
#define LIGHT_RELAY_PIN 9  // Active LOW relay for incubator lights
 
// Threshold values (adjust based on your sensors)
#define SOIL_DRY_THRESHOLD 500    // Below this = dry soil
#define LDR_DARK_THRESHOLD 300    // Below this = dark (lights should turn ON)
#define LDR_BRIGHT_THRESHOLD 400  // Above this = bright enough (lights can turn OFF)

// Timing constants
#define MIN_LIGHT_ON_TIME 28800000  // 8 hours in milliseconds (minimum daily light)
#define MAX_LIGHT_ON_TIME 57600000  // 16 hours in milliseconds (maximum daily light)

DHT dht(DHTPIN, DHTTYPE);

// State variables
unsigned long lightOnStartTime = 0;
unsigned long totalLightOnTime = 0;
bool lightsOn = false;
unsigned long lastDayReset = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  pinMode(PUMP_RELAY_PIN, OUTPUT);
  pinMode(LIGHT_RELAY_PIN, OUTPUT);
  
  digitalWrite(PUMP_RELAY_PIN, HIGH);  // Start with pump OFF (active LOW)
  digitalWrite(LIGHT_RELAY_PIN, HIGH); // Start with lights OFF (active LOW)
  
  lastDayReset = millis();
  
  Serial.println("=== Smart Plant Incubator System Started ===");
}
 
void loop() {
  // Read sensors
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  int soil = analogRead(SOIL_MOISTURE_PIN);
  int ldr = analogRead(LDR_PIN);
  
  // Print formatted sensor data
  Serial.println("--- Sensor Readings ---");
  
  if (!isnan(temp)) {
    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.println(" *C");
  } else {
    Serial.println("Temperature: ERROR");
  }
  
  if (!isnan(humidity)) {
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  } else {
    Serial.println("Humidity: ERROR");
  }
  
  Serial.print("Soil Moisture: ");
  Serial.println(soil);
  
  Serial.print("LDR Value: ");
  Serial.println(ldr);
  
  // Control water pump based on soil moisture
  if (soil < SOIL_DRY_THRESHOLD) {
    digitalWrite(PUMP_RELAY_PIN, LOW); // ON
    Serial.println("Status: Pump ON - Watering");
  } else {
    digitalWrite(PUMP_RELAY_PIN, HIGH); // OFF
    Serial.println("Status: Pump OFF");
  }
  
  // Control incubator lights based on LDR and daily light requirements
  controlLights(ldr);
  
  // Reset daily light counter every 24 hours
  if (millis() - lastDayReset >= 86400000) { // 24 hours
    totalLightOnTime = 0;
    lastDayReset = millis();
    Serial.println("Daily light timer reset");
  }
  
  // Print light status
  Serial.print("Lights: ");
  Serial.println(lightsOn ? "ON" : "OFF");
  
  Serial.print("Total Light Time Today: ");
  unsigned long currentTotal = totalLightOnTime;
  if (lightsOn) {
    currentTotal += (millis() - lightOnStartTime);
  }
  Serial.print(currentTotal / 3600000); // Convert to hours
  Serial.println(" hours");
  
  Serial.println("========================");
  Serial.println();
  
  delay(2000); // Wait 2 seconds between readings
}

/*
 * Function: controlLights
 * Description: Manages incubator lighting based on ambient light and daily requirements
 * Parameters: ldrValue - Current light sensor reading
 * Returns: void
 */

void controlLights(int ldrValue) {
  unsigned long currentTotal = totalLightOnTime;
  if (lightsOn) {
    currentTotal += (millis() - lightOnStartTime);
  }
  
  // Check if we've exceeded maximum light time
  if (currentTotal >= MAX_LIGHT_ON_TIME) {
    if (lightsOn) {
      digitalWrite(LIGHT_RELAY_PIN, HIGH); // Turn OFF
      totalLightOnTime += (millis() - lightOnStartTime);
      lightsOn = false;
      Serial.println("Light Control: Max daily light time reached - forcing OFF");
    }
    return;
  }
  
  // If it's dark and we haven't met minimum light requirement, turn lights ON
  if (ldrValue < LDR_DARK_THRESHOLD) {
    if (!lightsOn) {
      digitalWrite(LIGHT_RELAY_PIN, LOW); // Turn ON
      lightOnStartTime = millis();
      lightsOn = true;
      Serial.println("Light Control: Dark detected - Lights ON");
    }
  } 
  // If it's bright enough and we've met minimum light requirement, turn lights OFF
  else if (ldrValue > LDR_BRIGHT_THRESHOLD) {
    if (lightsOn && currentTotal >= MIN_LIGHT_ON_TIME) {
      digitalWrite(LIGHT_RELAY_PIN, HIGH); // Turn OFF
      totalLightOnTime += (millis() - lightOnStartTime);
      lightsOn = false;
      Serial.println("Light Control: Sufficient natural light - Lights OFF");
    } else if (lightsOn && currentTotal < MIN_LIGHT_ON_TIME) {
      Serial.println("Light Control: Keeping lights ON to meet minimum daily requirement");
    }
  }
}
