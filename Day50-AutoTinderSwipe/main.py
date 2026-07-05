from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from credentials import EMAIL, PASSWORD

# ---------------- SETUP ---------------- #

driver = webdriver.Chrome()

driver.maximize_window()

driver.get("https://tinder.com")

time.sleep(5)

# ---------------- LOGIN BUTTON ---------------- #

try:
    login_button = driver.find_element(
        By.XPATH,
        '//button[text()="Log in"]'
    )

    login_button.click()

except:
    print("Login button not found")

time.sleep(5)

# ---------------- FACEBOOK LOGIN ---------------- #

try:
    facebook_button = driver.find_element(
        By.XPATH,
        '//button[contains(@aria-label, "Facebook")]'
    )

    facebook_button.click()

except:
    print("Facebook login button not found")

time.sleep(5)

# ---------------- SWITCH TO FACEBOOK POPUP ---------------- #

base_window = driver.window_handles[0]
facebook_popup = driver.window_handles[1]

driver.switch_to.window(facebook_popup)

time.sleep(3)

# ---------------- ENTER EMAIL ---------------- #

try:
    email_input = driver.find_element(By.ID, "email")

    email_input.send_keys(EMAIL)

except:
    print("Email field not found")

# ---------------- ENTER PASSWORD ---------------- #

try:
    password_input = driver.find_element(By.ID, "pass")

    password_input.send_keys(PASSWORD)

except:
    print("Password field not found")

# ---------------- LOGIN ---------------- #

try:
    login = driver.find_element(By.NAME, "login")

    login.click()

except:
    print("Facebook login button not found")

time.sleep(8)

# ---------------- SWITCH BACK TO TINDER ---------------- #

driver.switch_to.window(base_window)

time.sleep(8)

# ---------------- HANDLE POPUPS ---------------- #

try:
    allow_location = driver.find_element(
        By.XPATH,
        '//button[contains(text(), "Allow")]'
    )

    allow_location.click()

except:
    print("Location popup not found")

time.sleep(3)

try:
    notifications = driver.find_element(
        By.XPATH,
        '//button[contains(text(), "Not interested")]'
    )

    notifications.click()

except:
    print("Notification popup not found")

time.sleep(3)

# ---------------- AUTO LIKE LOOP ---------------- #

while True:

    try:
        like_button = driver.find_element(
            By.XPATH,
            '//button[contains(@aria-label, "Like")]'
        )

        like_button.click()

        print("Liked profile")

        time.sleep(2)

    except:
        print("Could not like profile")

        time.sleep(2)