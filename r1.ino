#include <SPI.h>
#include <RF24.h>

RF24 radio(9, 10);

const byte address[6] = "00001";

// ===== DATA STRUCT =====
struct DataPacket {
  bool led1;
  bool led2;
  bool led3;
  int distance;
};

DataPacket data;

// Manual LEDs
int led1 = 19;
int led2 = 2;
int led3 = 3;

// Distance LEDs
int dled1 = 4;
int dled2 = 5;
int dled3 = 6;

void setup() {
  Serial.begin(9600);

  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
    digitalWrite(led1,HIGH);
  digitalWrite(led2,HIGH);
  digitalWrite(led3,HIGH);
  pinMode(dled1, OUTPUT);
  pinMode(dled2, OUTPUT);
  pinMode(dled3, OUTPUT);

  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_LOW);
  radio.startListening();
}

void loop() {

  if (radio.available()) {
    radio.read(&data, sizeof(data));

    // ===== MANUAL LED CONTROL =====
    digitalWrite(led1, data.led1);
    digitalWrite(led2, data.led2);
    digitalWrite(led3, data.led3);
    Serial.println(data.led1);
    updateDistanceLEDs(data.distance);
  }
}

// ===== HYSTERESIS =====
void updateDistanceLEDs(int distanceValue) {

  static bool led1State = HIGH;
  static bool led2State = HIGH;
  static bool led3State = HIGH;

  if (distanceValue > 110) led1State = LOW;
  else if (distanceValue < 90) led1State = HIGH;

  if (distanceValue > 160) led2State = LOW;
  else if (distanceValue < 140) led2State = HIGH;

  if (distanceValue > 180) led3State = LOW;
  else if (distanceValue < 160) led3State = HIGH;

  digitalWrite(dled1, led1State);
  digitalWrite(dled2, led2State);
  digitalWrite(dled3, led3State);
}

