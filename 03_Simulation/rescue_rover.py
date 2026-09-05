import random
import time

# =========================
# RESCUE RECOVER BOT
# Autonomous Search Simulation
# =========================

# Map symbols:
# . = empty space
# X = obstacle
# S = possible survivor
# R = rover

grid = [
    ["R", ".", ".", ".", ".", ".", "."],
    [".", ".", "X", "X", ".", ".", "."],
    [".", ".", ".", "X", ".", "X", "."],
    [".", "X", ".", ".", ".", "X", "."],
    [".", "X", ".", "X", ".", ".", "."],
    [".", ".", ".", ".", ".", ".", "S"]
]

rover_row = 0
rover_col = 0
survivor_row = 5
survivor_col = 6
visited = set()

directions = [
    (-1, 0, "UP"),
    (1, 0, "DOWN"),
    (0, -1, "LEFT"),
    (0, 1, "RIGHT")
]


def print_map():
    for row in range(len(grid)):
        line = ""
        for col in range(len(grid[row])):
            if row == rover_row and col == rover_col:
                line += "R "
            else:
                line += grid[row][col] + " "
        print(line)
    print()


def is_valid(row, col):
    if row < 0 or row >= len(grid):
        return False
    if col < 0 or col >= len(grid[0]):
        return False
    return grid[row][col] != "X"


def get_possible_moves():
    possible_moves = []

    for row_change, col_change, direction in directions:
        new_row = rover_row + row_change
        new_col = rover_col + col_change

        if is_valid(new_row, new_col):
            possible_moves.append((new_row, new_col, direction))

    return possible_moves


def choose_move():
    possible_moves = get_possible_moves()

    if not possible_moves:
        return None

    # Prefer unvisited cells so the rover searches new areas.
    unvisited_moves = [
        move for move in possible_moves
        if (move[0], move[1]) not in visited
    ]

    candidates = unvisited_moves if unvisited_moves else possible_moves

    # Among safe candidates, prefer positions closer to the simulated survivor.
    return min(
        candidates,
        key=lambda move: abs(move[0] - survivor_row)
        + abs(move[1] - survivor_col)
        + random.random() * 0.25
    )


print("================================")
print("     RESCUE RECOVER BOT")
print("     AUTONOMOUS SEARCH")
print("================================")
print()
print("Starting mission...")
print_map()

for step in range(100):
    visited.add((rover_row, rover_col))

    if grid[rover_row][rover_col] == "S":
        print("POSSIBLE SURVIVOR DETECTED!")
        print(f"Location: Row {rover_row}, Column {rover_col}")
        print(f"Steps taken: {step}")
        print()
        print("Sending rescue alert...")
        print("RESCUE TEAM NOTIFIED")
        break

    move = choose_move()

    if move is None:
        print("No safe movement available.")
        print("Search terminated.")
        break

    new_row, new_col, direction = move

    print(f"Step {step + 1}")
    print(f"Direction: {direction}")

    rover_row = new_row
    rover_col = new_col

    print(f"Position: Row {rover_row}, Column {rover_col}")
    print_map()

    time.sleep(0.2)
else:
    print("Search limit reached.")
    print("Possible survivor not found.")
