from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# -----------------------------
# GET TOPIC FROM USER
# -----------------------------

topic = input("What topic are you studying? ")

search_query = topic + " tutorial"


# -----------------------------
# OPEN CHROME
# -----------------------------

driver = webdriver.Chrome()

driver.get("https://duckduckgo.com/")

time.sleep(2)


# -----------------------------
# FIND SEARCH BOX
# -----------------------------

search_box = driver.find_element(
    By.NAME,
    "q"
)


# -----------------------------
# SEARCH FOR THE TOPIC
# -----------------------------

search_box.send_keys(search_query)

search_box.send_keys(Keys.RETURN)

time.sleep(3)


# -----------------------------
# FIND SEARCH RESULTS
# -----------------------------

results = driver.find_elements(
    By.CSS_SELECTOR,
    "a[data-testid='result-title-a']"
)


# -----------------------------
# SAVE THE RESULTS
# -----------------------------

with open(
    "study_resources.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        f"Study Resources for: {topic}\n"
    )

    file.write("=" * 50 + "\n\n")


    for number, result in enumerate(
        results[:5],
        start=1
    ):

        title = result.text
        link = result.get_attribute("href")

        file.write(
            f"{number}. {title}\n"
        )

        file.write(
            f"{link}\n\n"
        )


# -----------------------------
# SHOW RESULTS
# -----------------------------

print("\nStudy resources found:\n")

for number, result in enumerate(
    results[:5],
    start=1
):

    print(
        f"{number}. {result.text}"
    )

    print(
        result.get_attribute("href")
    )

    print()


# -----------------------------
# KEEP BROWSER OPEN
# -----------------------------

input(
    "Press Enter to close the browser..."
)

driver.quit()