from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


PROMISED_DOWN = 32
PROMISED_UP = 23

TWITTER_EMAIL = "manoghna.sms@gmail.com"
TWITTER_PASSWORD = "truebeauty09"

class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome() #create chrome browser instance
        self.down = 0
        self.up = 0 #store download and upload speeds


    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        go_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        go_button.click()
        time.sleep(60)
        download = self.driver.find_element(By.CLASS_NAME, "download-speed")
        upload = self.driver.find_element(By.CLASS_NAME, "upload-speed")

        # Store speeds in variables
        self.down = download.text
        self.up = upload.text

        # Print results in console
        print(f"Download Speed: {self.down}")
        print(f"Upload Speed: {self.up}")

    def tweet_at_provider(self):

        # Open X/Twitter login page
        self.driver.get("https://x.com/home")

        # Wait for page to load
        time.sleep(8)

        email_input = self.driver.find_element(
            By.NAME,
            "text"
        )
        email_input.send_keys(TWITTER_EMAIL)
        email_input.send_keys(Keys.ENTER)
        time.sleep(5)
        # Find password field
        password_input = self.driver.find_element(
            By.NAME,
            "password"
        )

        password_input.send_keys(TWITTER_PASSWORD) #typing password
        password_input.send_keys(Keys.ENTER)

        # Wait for login
        time.sleep(10)

        # CREATE TWEET MESSAGE
        tweet_message = (
            f"Hey Internet Provider, "
            f"why is my internet speed "
            f"{self.down}down/{self.up}up "
            f"when I pay for "
            f"{PROMISED_DOWN}down/"
            f"{PROMISED_UP}up?"
            )
        tweet_box = self.driver.find_element( #using By stratergy to locate tweet box
            By.XPATH,
            '//div[@data-testid="tweetTextarea_0"]'
        )

        tweet_box.click()

        tweet_box.send_keys(tweet_message) #type tweet
        time.sleep(3)

        #find tweet button
        tweet_button = self.driver.find_element(
            By.XPATH,
            '//button[@data-testid="tweetButtonInline"]'
        )

        # Click tweet button
        tweet_button.click()
        print("Tweet posted successfully!")


bot = InternetSpeedTwitterBot()

# Step 1 -> Get internet speed
bot.get_internet_speed()

# Step 2 -> Tweet complaint
bot.tweet_at_provider()





