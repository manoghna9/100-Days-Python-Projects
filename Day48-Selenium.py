from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome open after script finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# Open Python website
driver.get("https://www.python.org/")

# Find all event times
event_times = driver.find_elements(
    By.CSS_SELECTOR,
    ".event-widget time"
)

# Find all event names
event_names = driver.find_elements(
    By.CSS_SELECTOR,
    ".event-widget li a"
)

# Store events in a dictionary
events = {}

for n in range(len(event_times)):
    events[n] = {
        "time": event_times[n].text,
        "name": event_names[n].text
    }

print(events)

driver.quit()