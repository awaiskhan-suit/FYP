# Intelligent Appliances Control Using Computer Vision and Wireless Embedded System

### Touchless Smart Appliance Automation Through Hand Gesture Recognition

## Project Overview

This Final Year Design Project (FYDP) presents an intelligent, touchless electrical appliance control system that integrates Computer Vision, Artificial Intelligence techniques, and Wireless Embedded Systems.

The system enables users to control electrical appliances such as lights and DC fans through real-time hand gestures without physically touching switches, regulators, or remote controls.

Using a webcam, OpenCV, and MediaPipe, the system detects hand landmarks and calculates the distance between the thumb and index finger. Python processes this information and generates commands that are transmitted wirelessly through NRF24L01 transceiver modules to an Arduino Nano microcontroller.

The Arduino Nano processes the received commands and controls electrical appliances through relay modules.

In addition to gesture-based control, the system provides manual appliance control through a graphical user interface, automatic light control using an LDR sensor, and real-time electrical monitoring using current and voltage sensors.

**An important feature is that the system uses direct RF wireless communication and does not require an internet connection.**

## How Does the Project Work?

The complete system operates through the following process:

1. **Camera Input:** A webcam captures the user's hand movements in real time.
2. **Hand Tracking:** OpenCV and MediaPipe detect and track hand landmarks.
3. **Gesture Processing:** Python calculates the distance between the thumb and index finger.
4. **Command Generation:** The application converts the calculated distance into appliance control commands.
5. **Wireless Transmission:** NRF24L01 transmits the generated commands through radio frequency communication.
6. **Microcontroller Processing:** Arduino Nano receives and interprets the commands.
7. **Appliance Control:** Relay modules switch the connected LEDs and DC fans ON or OFF.
8. **Electrical Monitoring:** ACS712 and voltage divider circuits measure current and voltage.
9. **Power Calculation:** The application calculates power consumption and displays electrical readings through the GUI.

## Key Features

- Real-time hand gesture detection.
- Touchless electrical appliance control.
- Thumb and index finger distance measurement.
- Sequential ON/OFF appliance switching.
- Wireless communication using NRF24L01.
- Arduino Nano-based appliance control.
- Relay-based switching mechanism.
- Automatic light control using an LDR sensor.
- Manual ON/OFF control through the graphical interface.
- Real-time current and voltage monitoring.
- Power consumption calculation and display.
- Internet-independent operation.

## Technologies and Tools

### Software Technologies
- Python
- OpenCV
- MediaPipe
- PyQt5
- Embedded C/C++
- Arduino IDE
- PyCharm

### Hardware Components
- Arduino Nano (ATmega328)
- NRF24L01 Wireless Transceiver Modules
- Webcam
- LDR Sensor
- ACS712 Current Sensor
- Voltage Divider Circuit
- Relay Modules
- Optocouplers
- Voltage Regulator
- LEDs and DC Fans

## System Architecture

**Input Layer:** Webcam captures hand gestures.

**Processing Layer:** Python, OpenCV, and MediaPipe process visual information.

**Decision and Control Layer:** Python generates appliance control commands.

**Communication Layer:** NRF24L01 modules transmit commands wirelessly.

**Hardware Execution Layer:** Arduino Nano processes commands and controls relay modules.

**Monitoring Layer:** Sensors measure electrical parameters and provide readings to the graphical interface.

## Testing and Results

The developed system was evaluated using Black Box Testing and Integration Testing.

Testing covered:

- Real-time hand detection and tracking.
- Finger-distance measurement.
- Wireless command transmission.
- Relay-based appliance switching.
- Manual appliance control.
- Automatic LDR-based light control.
- Current and voltage measurement.
- Power consumption calculation.
- Graphical interface updates.

The integrated prototype demonstrated successful gesture-based appliance control and wireless communication, with an approximate response time of one second.

## Applications

- Smart Homes
- Hospitals and Healthcare Facilities
- Laboratories
- Offices
- Educational Environments
- Touchless Automation Systems

## Limitations and Future Improvements

The current system has certain limitations:

- Gesture detection can be affected by poor lighting.
- Webcam obstruction can reduce detection accuracy.
- NRF24L01 communication has a limited operating range.
- The system currently supports a limited number of appliances.

Future improvements may include advanced gesture recognition, support for additional appliances, improved wireless communication, and more precise fan speed and light brightness control.

## Academic Information

**Project Title:** Intelligent Appliances Control Using Computer Vision and Wireless Embedded System

**Degree:** BS Software Engineering

**University:** Sarhad University of Science and Information Technology, Peshawar

**Session:** 2022–2026

**Project Supervisor:** Dr. Shahid Latif

**Project Team:**
- Awais Khan
- Taha Amir

## Conclusion

This project demonstrates how Computer Vision and Wireless Embedded Technology can be integrated to develop an intelligent and touchless appliance control solution.

By combining real-time hand gesture recognition, wireless communication, embedded hardware, automatic sensing, and electrical monitoring, the system provides a practical approach to modern appliance automation without depending on internet connectivity.

**Developed as a Final Year Design Project (FYDP) – BS Software Engineering.**
