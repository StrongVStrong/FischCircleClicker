from ahk import AHK
import pyautogui
import time
import random
import keyboard
import math

# Initialize the AutoHotkey instance
ahk = AHK()

# Image to check
image = 'shake.png'

# Flag to control whether the script is running
running = False

# Track the last clicked positions
last_click_position = None
ignore_radius = 50  # Radius to ignore recently clicked spots
cooldown = 0.1  # Cooldown time between clicks

def distance(p1, p2):
    """
    Calculate the Euclidean distance between two points.
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_within_ignore_radius(x, y):
    """
    Check if the given position (x, y) is within the ignore radius.
    """
    global last_click_position
    if last_click_position is None:
        return False
    return distance(last_click_position, (x, y)) <= ignore_radius

def move_mouse_smoothly(start_x, start_y, target_x, target_y, duration=0.1):
    """
    Move the mouse smoothly from (start_x, start_y) to (target_x, target_y) over `duration` seconds.
    """
    steps = 10  # Keep steps low for speed, but enough for visible smoothness
    sleep_time = duration / steps  # Time to wait between each step
    delta_x = (target_x - start_x) / steps
    delta_y = (target_y - start_y) / steps

    for step in range(steps):
        intermediate_x = start_x + delta_x * step
        intermediate_y = start_y + delta_y * step
        ahk.mouse_move(intermediate_x, intermediate_y, relative=False)
        time.sleep(sleep_time)

    # Ensure the final position is reached
    ahk.mouse_move(target_x, target_y, relative=False)

def move_and_click_with_ahk(x, y):
    """
    Use AutoHotkey to move the mouse and perform a click with smooth motion.
    """
    global last_click_position, last_click_time

    # Add random offsets to make it look human
    offset_x = random.randint(-5, 5)  # Slight random offset for precision
    offset_y = random.randint(-5, 5)
    target_x = x + offset_x
    target_y = y + offset_y

    # Check if this position is within the ignore radius of the last clicked position
    if is_within_ignore_radius(target_x, target_y):
        print(f"Skipping position ({target_x}, {target_y}) within ignore radius")
        return

    # Get the current mouse position
    start_x, start_y = pyautogui.position()

    # Smoothly move the mouse to the target position
    move_mouse_smoothly(start_x, start_y, target_x, target_y, duration=0.1)  # Adjusted to 0.1 seconds

    # Perform a click
    ahk.click()

    # Store the clicked position
    last_click_position = (target_x, target_y)

    # Update the last click time
    last_click_time = time.time()

    print(f"Clicked at ({target_x}, {target_y})")

def toggle_running():
    """
    Toggle the running state with F6 key.
    """
    global running
    running = not running
    if running:
        print("Script started. Press F6 to stop.")
    else:
        print("Script stopped.")

# Bind F6 to start/stop the script
keyboard.add_hotkey("F6", toggle_running)

print("Press F6 to start or stop the script. Press Esc to exit.")

try:
    while True:
        if running:
            try:
                # Locate the image on the screen
                location = pyautogui.locateOnScreen(image, confidence=0.5)  # Lower confidence for better detection
                if location is not None:
                    print(f"ITS THERE ({image})")
                    # Get the center of the detected image
                    center_x, center_y = pyautogui.center(location)
                    
                    # Move and click using AutoHotkey
                    move_and_click_with_ahk(center_x, center_y)
            except pyautogui.ImageNotFoundException:
                # Handle the exception and continue
                print("its not there")
                pass
            except Exception as e:
                print(f"Unexpected error: {e}")
        time.sleep(0.01)  # Minimal delay to prevent high CPU usage
except KeyboardInterrupt:
    print("Exiting...")
