# 03 Simulation

The simulation stage allows the navigation and mission logic to be developed before hardware is available.

## Completed Simulations

### 1. Obstacle Avoidance

`obstacle_avoidance.py` simulates ultrasonic distance readings and basic movement decisions:

- Greater than 50 cm: move forward
- 30–50 cm: slow down
- Less than 30 cm: stop and turn

### 2. Grid Search

`search_simulation.py` models rover movement on a grid containing obstacles and a possible survivor location.

### 3. Autonomous Search

`rescue_rover.py` adds autonomous movement, visited-cell tracking, obstacle checking, and survivor detection.

### 4. Visual Mission Simulation

`visual_rover.py` provides a Pygame dashboard containing:

- Live rover map
- Obstacles and visited cells
- Autonomous navigation
- Simulated ultrasonic sensing
- Temperature readings
- PIR motion sensing
- GPS coordinates
- Camera status
- Battery simulation
- Search coverage percentage
- Obstacle events
- Mission log
- Possible survivor detection
- Rescue alert

## Running the Visual Simulation

Install Pygame:

```bash
pip install pygame
```

Then run:

```bash
python visual_rover.py
```

## Controls

- `SPACE`: pause/resume
- `R`: restart mission
- Close the window to exit
