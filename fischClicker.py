from ahk import AHK
import pyautogui
import time
import random
import keyboard
import math

ahk = AHK()

image = 'shake.png'

running = False

last_click_position = None
ignore_radius = 50
cooldown = 0.1

# Dist b/w points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_within_ignore_radius(x, y):
    global last_click_position
    if last_click_position is None:
        return False
    return distance(last_click_position, (x, y)) <= ignore_radius

# Smooth movement
def move_mouse_smoothly(start_x, start_y, target_x, target_y, duration=0.1):
    steps = 10
    sleep_time = duration / steps
    delta_x = (target_x - start_x) / steps
    delta_y = (target_y - start_y) / steps

    for step in range(steps):
        intermediate_x = start_x + delta_x * step
        intermediate_y = start_y + delta_y * step
        ahk.mouse_move(intermediate_x, intermediate_y, relative=False)
        time.sleep(sleep_time)

    ahk.mouse_move(target_x, target_y, relative=False)

# Smooth click
def move_and_click_with_ahk(x, y):
    global last_click_position, last_click_time
    offset_x = random.randint(-5, 5)
    offset_y = random.randint(-5, 5)
    target_x = x + offset_x
    target_y = y + offset_y

    if is_within_ignore_radius(target_x, target_y):
        print(f"Skipping position ({target_x}, {target_y}) (ignore radius)")
        return

    start_x, start_y = pyautogui.position()

    move_mouse_smoothly(start_x, start_y, target_x, target_y, duration=0.1)

    ahk.click()
    last_click_position = (target_x, target_y)
    last_click_time = time.time()

    print(f"Clicked at ({target_x}, {target_y})")

# Run prog w/ f6
def toggle_running():
    global running
    running = not running
    if running:
        print("Script started. Press F6 to stop.")
    else:
        print("Script stopped.")
keyboard.add_hotkey("F6", toggle_running)

print("Press F6 to start or stop the script. Press Esc to exit.")

try:
    while True:
        if running:
            try:
                location = pyautogui.locateOnScreen(image, confidence=0.5)
                if location is not None:
                    print(f"ITS THERE ({image})")
                    center_x, center_y = pyautogui.center(location)
                    move_and_click_with_ahk(center_x, center_y)
            except pyautogui.ImageNotFoundException:
                print("its not there")
                pass
            except Exception as e:
                print(f"Unexpected error: {e}")
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Exiting...")
