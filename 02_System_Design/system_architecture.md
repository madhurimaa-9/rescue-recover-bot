# System Architecture

## Overview

The Rescue Recover Bot is planned as a two-controller robotic system.

### Arduino UNO

Responsible for low-level rover control and basic sensors:

- Motor control through L298N
- Ultrasonic obstacle detection
- PIR motion sensing
- Temperature sensing
- Basic navigation decisions

### ESP32 Camera / Communication Controller

Responsible for:

- Camera streaming
- Wireless communication
- Sending telemetry to a laptop or phone
- Supporting the monitoring interface

### GPS

Provides the rover's approximate position so detected events can be associated with coordinates.

## Data Flow

```text
Sensors
   |
   v
Arduino UNO -----> ESP32 / Communication -----> Laptop / Phone
   |                         |
   v                         v
Motors                   Camera Stream

GPS ---------------------> Telemetry
```

## Detection Concept

The prototype should report a **possible survivor** rather than claim definitive human detection. A future hardware implementation can combine motion, temperature, and camera information to reduce false positives.

## Design Principle

The system is being developed in stages so each subsystem can be tested independently before integration.
