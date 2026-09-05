import pygame
import random
import time

pygame.init()

# ============================================================
# RESCUE RECOVER BOT
# Milestone 3
# Mission Dashboard + Search Algorithm
# ============================================================

WIDTH = 1150
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue Recover Bot")
clock = pygame.time.Clock()

# ============================================================
# COLORS
# ============================================================

WHITE = (245, 245, 245)
BLACK = (25, 25, 25)
GREY = (170, 170, 170)
LIGHT_GREY = (225, 225, 225)
BLUE = (50, 120, 220)
DARK_BLUE = (35, 70, 130)
RED = (220, 50, 50)
GREEN = (50, 175, 90)
YELLOW = (235, 190, 40)
ORANGE = (235, 125, 40)
PURPLE = (130, 80, 190)

# ============================================================
# FONTS
# ============================================================

font = pygame.font.SysFont("Arial", 19)
small_font = pygame.font.SysFont("Arial", 15)
title_font = pygame.font.SysFont("Arial", 27, bold=True)
big_font = pygame.font.SysFont("Arial", 35, bold=True)

# ============================================================
# MAP
# ============================================================

grid = [
    [".", ".", ".", ".", ".", ".", ".", "."],
    [".", ".", "X", "X", ".", ".", ".", "."],
    [".", ".", ".", "X", ".", "X", ".", "."],
    [".", "X", ".", ".", ".", "X", ".", "."],
    [".", "X", ".", "X", ".", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", ".", "S"],
]

ROWS = len(grid)
COLS = len(grid[0])
CELL_SIZE = 80
GRID_X = 35
GRID_Y = 85

# ============================================================
# ROVER
# ============================================================

rover_row = 0
rover_col = 0
direction = "RIGHT"
visited = set()
steps = 0
obstacles_detected = 0

# ============================================================
# MISSION
# ============================================================

mission_running = True
mission_complete = False
paused = False
mission_start_time = time.time()
mission_end_time = None
status = "SEARCHING"
last_action = "Mission started"

# ============================================================
# SURVIVOR
# ============================================================

survivor_row = 5
survivor_col = 7
possible_survivor = False
alert_sent = False

# ============================================================
# SENSORS
# ============================================================

ultrasonic_distance = 100.0
temperature = 25.0
motion_detected = False
camera_active = True

# ============================================================
# BATTERY
# ============================================================

battery = 100.0

# ============================================================
# GPS
# ============================================================

BASE_LAT = 13.0827
BASE_LON = 80.2707
GPS_STEP = 0.0001
gps_lat = BASE_LAT
gps_lon = BASE_LON

# ============================================================
# MISSION LOG
# ============================================================

mission_log = []


def add_log(message):
    mission_log.append(message)
    if len(mission_log) > 8:
        mission_log.pop(0)


# ============================================================
# DRAWING
# ============================================================

def draw_text(text, x, y, used_font=font):
    surface = used_font.render(text, True, BLACK)
    screen.blit(surface, (x, y))


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            x = GRID_X + col * CELL_SIZE
            y = GRID_Y + row * CELL_SIZE

            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

            if (row, col) in visited:
                pygame.draw.rect(
                    screen,
                    LIGHT_GREY,
                    (x + 3, y + 3, CELL_SIZE - 6, CELL_SIZE - 6)
                )

            if grid[row][col] == "X":
                pygame.draw.rect(
                    screen,
                    DARK_BLUE,
                    (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10)
                )

            if grid[row][col] == "S":
                pygame.draw.circle(
                    screen,
                    RED,
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    22
                )
                draw_text("S", x + 33, y + 25)

            pygame.draw.rect(
                screen,
                GREY,
                (x, y, CELL_SIZE, CELL_SIZE),
                2
            )


def draw_rover():
    x = GRID_X + rover_col * CELL_SIZE
    y = GRID_Y + rover_row * CELL_SIZE
    center_x = x + CELL_SIZE // 2
    center_y = y + CELL_SIZE // 2

    pygame.draw.rect(
        screen,
        BLUE,
        (x + 15, y + 15, CELL_SIZE - 30, CELL_SIZE - 30),
        border_radius=10
    )

    if direction == "UP":
        points = [
            (center_x, y + 10),
            (center_x - 10, y + 30),
            (center_x + 10, y + 30)
        ]
    elif direction == "DOWN":
        points = [
            (center_x, y + CELL_SIZE - 10),
            (center_x - 10, y + CELL_SIZE - 30),
            (center_x + 10, y + CELL_SIZE - 30)
        ]
    elif direction == "LEFT":
        points = [
            (x + 10, center_y),
            (x + 30, center_y - 10),
            (x + 30, center_y + 10)
        ]
    else:
        points = [
            (x + CELL_SIZE - 10, center_y),
            (x + CELL_SIZE - 30, center_y - 10),
            (x + CELL_SIZE - 30, center_y + 10)
        ]

    pygame.draw.polygon(screen, WHITE, points)


# ============================================================
# NAVIGATION
# ============================================================

def is_valid(row, col):
    if row < 0 or row >= ROWS:
        return False
    if col < 0 or col >= COLS:
        return False
    if grid[row][col] == "X":
        return False
    return True


def get_possible_moves():
    directions = [
        (-1, 0, "UP"),
        (1, 0, "DOWN"),
        (0, -1, "LEFT"),
        (0, 1, "RIGHT")
    ]

    possible = []
    for row_change, col_change, move_direction in directions:
        new_row = rover_row + row_change
        new_col = rover_col + col_change

        if is_valid(new_row, new_col):
            possible.append((new_row, new_col, move_direction))

    return possible


def choose_move():
    possible_moves = get_possible_moves()

    if not possible_moves:
        return None

    unvisited = []
    for move in possible_moves:
        new_row, new_col, move_direction = move
        if (new_row, new_col) not in visited:
            unvisited.append(move)

    if unvisited:
        best_move = None
        best_score = float("inf")

        for move in unvisited:
            new_row, new_col, move_direction = move
            distance = (
                abs(survivor_row - new_row)
                + abs(survivor_col - new_col)
            )
            score = distance + random.uniform(0, 0.3)

            if score < best_score:
                best_score = score
                best_move = move

        return best_move

    return random.choice(possible_moves)


# ============================================================
# GPS
# ============================================================

def update_gps():
    global gps_lat, gps_lon
    gps_lat = BASE_LAT + rover_row * GPS_STEP
    gps_lon = BASE_LON + rover_col * GPS_STEP


# ============================================================
# ULTRASONIC SENSOR
# ============================================================

def simulate_ultrasonic():
    global ultrasonic_distance, obstacles_detected

    ultrasonic_distance = random.uniform(35, 100)

    if direction == "RIGHT":
        next_row = rover_row
        next_col = rover_col + 1
    elif direction == "LEFT":
        next_row = rover_row
        next_col = rover_col - 1
    elif direction == "UP":
        next_row = rover_row - 1
        next_col = rover_col
    else:
        next_row = rover_row + 1
        next_col = rover_col

    if not is_valid(next_row, next_col):
        ultrasonic_distance = random.uniform(10, 25)
        obstacles_detected += 1
        add_log(f"Obstacle detected at {ultrasonic_distance:.0f} cm")


# ============================================================
# ENVIRONMENT
# ============================================================

def simulate_environment():
    global temperature, motion_detected, possible_survivor

    temperature = random.uniform(24, 31)
    motion_detected = False

    if rover_row == survivor_row and rover_col == survivor_col:
        temperature = random.uniform(35.5, 37.5)
        motion_detected = True

    if motion_detected and temperature >= 34:
        possible_survivor = True
    else:
        possible_survivor = False


# ============================================================
# BATTERY
# ============================================================

def update_battery():
    global battery
    battery -= 0.015
    if battery < 0:
        battery = 0


# ============================================================
# SURVIVOR ALERT
# ============================================================

def send_alert():
    global alert_sent, status, mission_complete, mission_end_time

    if possible_survivor and not alert_sent:
        alert_sent = True
        status = "SURVIVOR DETECTED"
        mission_complete = True
        mission_end_time = time.time()

        add_log("Possible survivor detected")
        add_log("GPS location recorded")
        add_log("Rescue alert sent")

        print()
        print("========================================")
        print("       RESCUE RECOVER BOT")
        print("========================================")
        print("POSSIBLE SURVIVOR DETECTED")
        print(f"GPS: {gps_lat:.4f}, {gps_lon:.4f}")
        print(f"Temperature: {temperature:.1f} C")
        print("Motion: DETECTED")
        print("Camera: ACTIVE")
        print("RESCUE ALERT SENT")
        print("========================================")


# ============================================================
# DASHBOARD
# ============================================================

def draw_sidebar():
    sidebar_x = 720
    sidebar_y = 20

    pygame.draw.rect(screen, WHITE, (sidebar_x, sidebar_y, 405, 680))
    pygame.draw.rect(screen, GREY, (sidebar_x, sidebar_y, 405, 680), 2)

    draw_text("RESCUE RECOVER BOT", sidebar_x + 20, sidebar_y + 20, title_font)
    draw_text("AUTONOMOUS SEARCH SYSTEM", sidebar_x + 20, sidebar_y + 57, small_font)

    draw_text("MISSION STATUS", sidebar_x + 20, sidebar_y + 100, font)
    status_color = RED if possible_survivor else GREEN
    status_surface = font.render(status, True, status_color)
    screen.blit(status_surface, (sidebar_x + 20, sidebar_y + 130))

    draw_text("BATTERY", sidebar_x + 20, sidebar_y + 175, font)
    pygame.draw.rect(screen, LIGHT_GREY, (sidebar_x + 20, sidebar_y + 207, 250, 20))
    pygame.draw.rect(
        screen,
        GREEN if battery > 25 else RED,
        (sidebar_x + 20, sidebar_y + 207, int(250 * battery / 100), 20)
    )
    draw_text(f"{battery:.1f}%", sidebar_x + 280, sidebar_y + 205, small_font)

    draw_text("SENSORS", sidebar_x + 20, sidebar_y + 255, font)
    draw_text(f"Ultrasonic: {ultrasonic_distance:.1f} cm", sidebar_x + 20, sidebar_y + 285, small_font)
    draw_text(f"Temperature: {temperature:.1f} C", sidebar_x + 20, sidebar_y + 310, small_font)

    motion_text = "DETECTED" if motion_detected else "NONE"
    draw_text(f"PIR Motion: {motion_text}", sidebar_x + 20, sidebar_y + 335, small_font)

    camera_text = "ACTIVE" if camera_active else "OFF"
    draw_text(f"Camera: {camera_text}", sidebar_x + 20, sidebar_y + 360, small_font)

    draw_text("GPS LOCATION", sidebar_x + 20, sidebar_y + 400, font)
    draw_text(f"Latitude:  {gps_lat:.4f}", sidebar_x + 20, sidebar_y + 430, small_font)
    draw_text(f"Longitude: {gps_lon:.4f}", sidebar_x + 20, sidebar_y + 455, small_font)

    draw_text("SEARCH DATA", sidebar_x + 20, sidebar_y + 495, font)

    coverage = (len(visited) / ((ROWS * COLS) - 5)) * 100
    if coverage > 100:
        coverage = 100

    draw_text(f"Coverage: {coverage:.1f}%", sidebar_x + 20, sidebar_y + 525, small_font)
    draw_text(f"Steps: {steps}", sidebar_x + 20, sidebar_y + 550, small_font)
    draw_text(f"Obstacles: {obstacles_detected}", sidebar_x + 20, sidebar_y + 575, small_font)

    draw_text("SPACE = Pause / Resume", sidebar_x + 20, sidebar_y + 615, small_font)
    draw_text("R = Restart Mission", sidebar_x + 20, sidebar_y + 640, small_font)


# ============================================================
# MISSION LOG WINDOW
# ============================================================

def draw_log():
    log_x = 35
    log_y = 590

    pygame.draw.rect(screen, WHITE, (log_x, log_y, 650, 110))
    pygame.draw.rect(screen, GREY, (log_x, log_y, 650, 110), 2)

    draw_text("MISSION LOG", log_x + 10, log_y + 8, small_font)

    y = log_y + 32
    for message in mission_log[-5:]:
        draw_text("• " + message, log_x + 10, y, small_font)
        y += 15


# ============================================================
# RESTART
# ============================================================

def restart():
    global rover_row, rover_col, direction, visited
    global steps, obstacles_detected, mission_complete, paused
    global mission_start_time, mission_end_time, status
    global alert_sent, battery, mission_log, possible_survivor

    rover_row = 0
    rover_col = 0
    direction = "RIGHT"
    visited = set()
    steps = 0
    obstacles_detected = 0
    mission_complete = False
    paused = False
    mission_start_time = time.time()
    mission_end_time = None
    status = "SEARCHING"
    alert_sent = False
    possible_survivor = False
    battery = 100
    mission_log = []
    add_log("Mission restarted")


# ============================================================
# STARTUP
# ============================================================

add_log("Autonomous search initiated")
add_log("Sensors online")
add_log("Camera online")
add_log("GPS initialized")

last_move_time = time.time()

# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    status = "PAUSED"
                    add_log("Mission paused")
                else:
                    status = "SEARCHING"
                    add_log("Mission resumed")

            if event.key == pygame.K_r:
                restart()

    if not paused and not mission_complete:
        simulate_ultrasonic()
        simulate_environment()
        update_gps()
        update_battery()

        if possible_survivor:
            send_alert()

        elif battery <= 0:
            status = "BATTERY EMPTY"
            mission_complete = True
            mission_end_time = time.time()
            add_log("Battery depleted")

        else:
            current_time = time.time()

            if current_time - last_move_time >= 0.5:
                visited.add((rover_row, rover_col))
                move = choose_move()

                if move is None:
                    status = "SEARCH COMPLETE"
                    mission_complete = True
                    mission_end_time = time.time()
                    add_log("No unexplored route available")

                else:
                    new_row, new_col, new_direction = move
                    rover_row = new_row
                    rover_col = new_col
                    direction = new_direction
                    steps += 1
                    last_action = f"Moving {direction}"
                    add_log(f"Moved {direction} to ({rover_row},{rover_col})")
                    last_move_time = current_time

    screen.fill(LIGHT_GREY)
    draw_text("RESCUE RECOVER BOT", GRID_X, 25, title_font)
    draw_grid()
    draw_rover()
    draw_sidebar()
    draw_log()

    if mission_complete:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 175))
        screen.blit(overlay, (0, 0))

        if possible_survivor:
            draw_text("POSSIBLE SURVIVOR DETECTED", 225, 220, big_font)
            draw_text("GPS LOCATION RECORDED", 290, 270, font)
            draw_text("RESCUE ALERT SENT", 315, 305, font)
            draw_text(f"GPS: {gps_lat:.4f}, {gps_lon:.4f}", 290, 340, font)
            draw_text(f"Temperature: {temperature:.1f} C", 300, 375, font)

        elif battery <= 0:
            draw_text("MISSION STOPPED", 350, 260, big_font)
            draw_text("BATTERY DEPLETED", 365, 310, font)

        else:
            draw_text("SEARCH COMPLETE", 350, 260, big_font)

        draw_text("Press R to restart mission", 350, 420, small_font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
