#To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

from datetime import datetime
import pandas
import random
import smtplib

# ---------------------------- EMAIL DETAILS ------------------------------- #

MY_EMAIL = "your_email@gmail.com"
MY_PASSWORD = "your_app_password"

# ---------------------------- DATE CHECK ------------------------------- #

today = datetime.now()
today_tuple = (today.month, today.day)

# ---------------------------- READ CSV ------------------------------- #

data = pandas.read_csv("/Users/suma/code/Gitdemo/100-Days-PythonProj/Day32-BirthdayWisher&Email/birthdays.csv")

# Create dictionary:
# (month, day) -> entire row
birthdays_dict = {
    (row["month"], row["day"]): row
    for (index, row) in data.iterrows()
}

# ---------------------------- FIND BIRTHDAY ------------------------------- #

if today_tuple in birthdays_dict:

    birthday_person = birthdays_dict[today_tuple]

    # Pick a random letter template
    random_letter = random.randint(1, 3)

    with open(f"letter_templates/letter_{random_letter}.txt") as letter_file:
        letter_contents = letter_file.read()

        # Replace placeholder with person's name
        letter_contents = letter_contents.replace(
            "[NAME]",
            birthday_person["name"]
        )

    # ---------------------------- SEND EMAIL ------------------------------- #

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()

        connection.login(
            user=MY_EMAIL,
            password=MY_PASSWORD
        )

        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=f"Subject:Happy Birthday!\n\n{letter_contents}"
        )

        print("Birthday email sent successfully!")