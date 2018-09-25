#include <Wire.h>
// hardwares
#define pumpPin A3
#define lightSensorPin A2
#define soilMoisturePin A1
#define thermistorPin A0

int thermBeta = 3950;
int thermResistance = 10;

// watering options
bool autoOpt;
char startWater = 'n';
int threshold;

void setup() {
  Serial.begin(9600);
  pinMode(pumpPin, OUTPUT);
  pinMode(lightSensorPin, INPUT);
  pinMode(soilMoisturePin, INPUT);
  pinMode(thermistorPin, INPUT);
  autoOpt = false;
  threshold = 20;
}

void loop() {
  delay(1000);
  Serial.println();
  long thermVal = 1023 - analogRead(thermistorPin);
  long soilVal = analogRead(soilMoisturePin);
  long lightVal = analogRead(lightSensorPin);
  shouldWater(soilVal);
  String tempOutput = getTempReadings(thermVal);
  String soilOutput = "\"soil_moisture\" : "+String(soilVal)+", ";
  String lightOutput = "\"light_level\" : "+String(normalizeLightVal(lightVal))+" }";
  String json = tempOutput+soilOutput+lightOutput;
  Serial.println(json);
}

void shouldWater(long soilVal) {
  if (autoOpt) {
    waterPlant(soilVal);
  } else {
    if (soilVal <= threshold) {
      Serial.println("{\"user\": Soil moisture is below normal. Would you like to water plant? (y or n) }");
      String response = Serial.readString();
      response.toLowerCase();
      startWater = response[0];
      if (startWater == 'y') {
        Serial.println("Detected response: "+response);
        waterPlant(soilVal);
      }
    } else {
      analogWrite(pumpPin, 0);
      startWater = 'n';
    }
  }
}

void waterPlant(long soilVal) {
  if (soilVal <= threshold) {
    Serial.println("Watering plant... ");
    analogWrite(pumpPin, 1023);
    // runs the water pump for 10 seconds.
    delay(5000);
  } else {
     analogWrite(pumpPin, 0);
  }
}

String getTempReadings(long thermVal) {
      float cTemp = getTempC(thermVal);
      float fTemp = getTempF(cTemp);
      float kTemp = getTempK(fTemp);
      return "{ \"temperature\" : { \"c\":"+String(cTemp)+", \"f\":"+String(fTemp)+", \"k\":"+String(kTemp)+" }, ";
}

float normalizeLightVal(long lightVal) {
  return 1025 - lightVal;  
}

float getTempC(long rawVal) {
  return thermBeta /(log((1025.0 * 10 / rawVal - 10) / 10) + thermBeta / 298.0) - 273.0;
}

float getTempF(float tempC) {
  return 1.8 * tempC + 32.0;
}

float getTempK(float tempF) {
  return (((tempF - 32) * 5) / 9) + 273.15;
}
