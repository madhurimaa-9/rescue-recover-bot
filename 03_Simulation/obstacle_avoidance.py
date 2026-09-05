dis = [100, 80, 65, 45, 35, 25, 18, 60, 75, 100]
front = 15
left = 25
right = 70
for distance in dis:
    print(f"Obstacle distance: {distance} cm")

    if distance > 50:
        print('Move forward.')
    elif distance in range(30,51):
        print('Slow down.')
    elif distance < 30:
        print("stop!. obstacle detected.")
        print('Turning...')
        if front < 30:
            if left > right:
                print('Turn left')
            else:
                print('Turn right')
            print('Move forward.')
    print()
