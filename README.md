# Rescue Recover Bot

## Autonomous Search-and-Rescue Rover

A low-cost autonomous rover designed to assist with search-and-rescue scenarios by combining autonomous navigation, obstacle detection, environmental sensing, GPS positioning, camera monitoring, and possible survivor detection.

> **Project status:** Software simulation complete. Hardware prototype is the next stage.

## Project Goals

The rover is designed to:

- Navigate an area autonomously
- Detect and avoid obstacles
- Search an area systematically
- Detect a possible survivor using simulated motion and temperature signals
- Monitor temperature and motion sensors
- Stream camera footage in the hardware version
- Record GPS coordinates
- Send sensor information to a monitoring device
- Generate a mission log and rescue alert

## Current Progress

| Milestone | Status |
|---|---|
| Basic obstacle-avoidance simulation | Complete |
| Grid-based search simulation | Complete |
| Autonomous search simulation | Complete |
| Visual Pygame simulation | Complete |
| Sensor-integrated simulation | Complete |
| Mission dashboard and logging | Complete |
| Hardware architecture | In progress |
| Arduino motor control | Planned |
| Sensor integration | Planned |
| Camera system | Planned |
| Full hardware field test | Planned |

## System Concept

```text
                 +----------------------+
                 |   Monitoring Device   |
                 |  Laptop / Phone       |
                 +----------+-----------+
                            |
                     Wi-Fi / Serial
                            |
                 +----------v-----------+
                 | Communication /      |
                 | Camera Controller    |
                 | ESP32                 |
                 +----------+-----------+
                            |
                 +----------v-----------+
                 |     Arduino UNO      |
                 | Motor + Sensor Logic |
                 +----+-------------+---+
                      |             |
                +-----v---+   +-----v------+
                | L298N   |   | Sensors     |
                | Motor   |   | Ultrasonic  |
                | Driver  |   | PIR / Temp  |
                +----+----+   | GPS         |
                     |        +-------------+
                  Motors
```

## Hardware Plan

The planned prototype uses:

- Arduino UNO
- L298N motor driver
- DC geared motors and rover chassis
- HC-SR04 ultrasonic sensor
- PIR motion sensor
- MLX90614 non-contact temperature sensor
- GPS module
- ESP32-CAM or equivalent ESP32 camera board
- Battery and power regulation system

The exact component choices and wiring will be documented before hardware assembly.

## Simulation

The simulation is written in Python using Pygame. It models rover movement, obstacle detection, search coverage, temperature, motion, GPS coordinates, battery level, mission logging, and possible survivor detection.

A possible survivor is **not** treated as guaranteed human identification. In the simulation, detection is based on a combination of simulated motion and elevated temperature signals.

## Repository Structure

```text
rescue-recover-bot/
│
├── 01_Research/
│   └── README.md
├── 02_System_Design/
│   ├── system_architecture.md
│   └── components.md
├── 03_Simulation/
│   ├── README.md
│   └── [simulation source files]
├── 04_Arduino/
│   └── README.md
├── 05_Testing/
│   └── README.md
├── 06_Documentation/
│   └── README.md
├── README.md
└── .gitignore
```

## Limitations

This is an educational prototype. The simulation does not prove reliable real-world survivor identification, GPS accuracy, autonomous navigation in complex terrain, or reliable rescue operation. Hardware testing will be required to validate each subsystem.

## Future Improvements

- Better search and coverage algorithms
- Real sensor fusion
- More robust obstacle avoidance
- Live camera dashboard
- Wireless telemetry
- Improved GPS mapping
- Hardware battery monitoring
- Real-world field testing
- More reliable survivor-detection methods

## Author

Madhurimaa

High-school engineering project focused on robotics, programming, autonomous systems, and search-and-rescue technology.
