import random
import time

# =========================
# RESCUE RECOVER BOT
# Autonomous Search Simulation
# =========================

# Map
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

# Rover starting position
rover_row = 0
rover_col = 0

# Track cells the rover has visited
visited = set()

# Directions
directions = [
    (-1, 0, "UP"),
    (1, 0, "DOWN"),
    (0, -1, "LEFT"),
    (0, 1, "RIGHT")
]


def print_map():
    """Display the current map."""

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
    """Check whether a position is inside the map and not an obstacle."""

    if row < 0 or row >= len(grid):
        return False

    if col < 0 or col >= len(grid[0]):
        return False

    if grid[row][col] == "X":
        return False

    return True


def get_possible_moves():
    """Find all safe cells around the rover."""

    possible_moves = []

    for row_change, col_change, direction in directions:

        new_row = rover_row + row_change
        new_col = rover_col + col_change

        if is_valid(new_row, new_col):
            possible_moves.append(
                (new_row, new_col, direction)
            )

    return possible_moves


def choose_move():
    """Choose an unvisited safe location."""

    possible_moves = get_possible_moves()

    # Prefer cells that haven't been visited
    unvisited_moves = []

    for move in possible_moves:
        new_row, new_col, direction = move

        if (new_row, new_col) not in visited:
            unvisited_moves.append(move)

    if unvisited_moves:
        return random.choice(unvisited_moves)

    if possible_moves:
        return random.choice(possible_moves)

    return None


# =========================
# MAIN SEARCH LOOP
# =========================

print("================================")
print("     RESCUE RECOVER BOT")
print("     SEARCH SIMULATION")
print("================================")
print()

print("Starting mission...")
print_map()

for step in range(100):

    # Mark current location as visited
    visited.add((rover_row, rover_col))

    # Check for survivor
    if grid[rover_row][rover_col] == "S":

        print("SURVIVOR DETECTED!")
        print(
            f"Location: Row {rover_row}, "
            f"Column {rover_col}"
        )
        print(f"Steps taken: {step}")
        print()
        print("Sending rescue alert...")
        print("RESCUE TEAM NOTIFIED")
        break

    # Find next safe movement
    move = choose_move()

    if move is None:
        print("No safe movement available.")
        print("Search terminated.")
        break

    new_row, new_col, direction = move

    print(f"Step {step + 1}")
    print(f"Direction: {direction}")

    # Move rover
    rover_row = new_row
    rover_col = new_col

    print(
        f"Position: Row {rover_row}, "
        f"Column {rover_col}"
    )

    print_map()

    time.sleep(0.3)

else:
    print("Search limit reached.")
    print("Survivor not found.")
