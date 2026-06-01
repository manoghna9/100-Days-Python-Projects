import smtplib
import datetime as dt
import random

MY_EMAIL = "your_email@gmail.com"
MY_PASSWORD = "your_app_password"

now = dt.datetime.now()
weekday = now.weekday()
print("Program started")
print(f"Weekday = {weekday}")

if weekday==6:
    print("Inside if block")
    with open("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day32-Emails/quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)

    print(quote)
    print("opening SMTP connection")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Monday Motivation\n\n{quote}"
        )
        print("EMAIL SENT")


