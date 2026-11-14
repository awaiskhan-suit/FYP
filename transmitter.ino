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

String cmd = "";

void setup() {
  Serial.begin(9600);

  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW);
  radio.stopListening();
}

void loop() {

  // ===== READ SERIAL FROM PYTHON =====
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      processCommand(cmd);
      cmd = "";
    } else {
      cmd += c;
    }
  }

  // ===== SEND DATA =====
  radio.write(&data, sizeof(data));

  delay(100);
}

// ===== PROCESS COMMAND =====
void processCommand(String cmd) {

  cmd.trim();

  if (cmd == "LED1_ON") data.led1 = false;
  else if (cmd == "LED1_OFF") data.led1 = true;

  else if (cmd == "LED2_ON") data.led2 = false;
  else if (cmd == "LED2_OFF") data.led2 = true;

  else if (cmd == "LED3_ON") data.led3 = false;
  else if (cmd == "LED3_OFF") data.led3 = true;

  else if (cmd.startsWith("DIST:")) {
    data.distance = cmd.substring(5).toInt();
  }
}
