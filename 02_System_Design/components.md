# Hardware Components

| Component | Purpose | Planned Controller |
|---|---|---|
| Arduino UNO | Main low-level controller | Arduino UNO |
| L298N | Dual-channel motor driver | Arduino UNO |
| DC geared motors | Rover movement | L298N |
| Rover chassis | Mechanical platform | — |
| HC-SR04 | Obstacle distance measurement | Arduino UNO |
| PIR sensor | Motion detection | Arduino UNO |
| MLX90614 | Non-contact temperature measurement | Arduino UNO |
| GPS module | Position tracking | Arduino UNO / communication controller |
| ESP32-CAM | Camera and wireless video | ESP32 |
| Battery system | Power supply | — |
| Jumper wires / connectors | Electrical connections | — |

## Selection Notes

The component list is designed around a low-cost educational prototype. Exact models, quantities, voltage requirements, and power connections will be finalized before hardware assembly.

## Important Power Note

The motors and logic electronics should not simply be connected to the same power rail without checking voltage and current requirements. The final design will document separate regulated supplies or appropriate power distribution where necessary.
