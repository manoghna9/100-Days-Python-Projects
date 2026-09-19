import pyautogui
from PIL import ImageGrab
import time


# ==========================================================
# SETTINGS
# ==========================================================

# The area of the screen where we will look for obstacles.
# We will adjust these values after seeing your game.
GAME_AREA = (0, 300, 1200, 500)

# How far in front of the dinosaur we check for a cactus.
CHECK_WIDTH = 180

# Height of the area where a cactus is expected to appear.
CHECK_HEIGHT = 80


# ==========================================================
# TAKE A SCREENSHOT
# ==========================================================

def take_screenshot():
    """
    Takes a screenshot of the game area.
    """

    screenshot = ImageGrab.grab(
        bbox=GAME_AREA
    )

    return screenshot


# ==========================================================
# CHECK FOR AN OBSTACLE
# ==========================================================

def obstacle_detected(image):
    """
    Looks at pixels in front of the dinosaur.

    The Chrome dinosaur game has a light background
    and dark obstacles.

    Therefore, we look for dark pixels.
    """

    width, height = image.size

    # Look at the area where a cactus should appear.
    start_x = 250
    end_x = min(
        start_x + CHECK_WIDTH,
        width
    )

    start_y = 20
    end_y = min(
        start_y + CHECK_HEIGHT,
        height
    )

    for x in range(start_x, end_x):

        for y in range(start_y, end_y):

            pixel = image.getpixel((x, y))

            red, green, blue = pixel[:3]

            # Dark pixels represent the cactus/obstacle.
            if red < 100 and green < 100 and blue < 100:

                return True

    return False


# ==========================================================
# JUMP
# ==========================================================

def jump():
    """
    Press the space bar to make the dinosaur jump.
    """

    pyautogui.press("space")


# ==========================================================
# MAIN BOT
# ==========================================================

def main():

    print("Starting T-Rex bot...")
    print("Place the Chrome game on screen.")
    print("Starting in 3 seconds...")

    time.sleep(3)

    print("Bot started!")

    while True:

        # Take a screenshot
        screenshot = take_screenshot()

        # Check whether an obstacle is approaching
        if obstacle_detected(screenshot):

            print("Obstacle detected! Jumping!")

            jump()

            # Give the dinosaur a little time
            # before checking again.
            time.sleep(0.1)

        else:

            # Keep checking the screen
            time.sleep(0.01)


# ==========================================================
# START PROGRAM
# ==========================================================

if __name__ == "__main__":
    main()