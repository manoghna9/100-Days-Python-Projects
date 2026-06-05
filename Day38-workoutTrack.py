import requests
from datetime import datetime

# ---------------------------- USER DETAILS ---------------------------- #

APP_ID = "app_b09e9efda4214e7393e56d3d"
API_KEY = "nix_live_Gn5nNGMfaTgT5Lasx4XMxMzT6UI6YN63"

SHEETY_ENDPOINT = "https://api.sheety.co/7b8cb3ebb12c41d15fbf6258c835ea31/workoutTracking/sheet1"
SHEETY_TOKEN = "YOUR_SHEETY_BEARER_TOKEN"

GENDER = "male"
WEIGHT_KG = 70
HEIGHT_CM = 175
AGE = 20

# ---------------------------- EXERCISE INPUT ---------------------------- #

exercise_text = input("Tell me which exercises you did: ")

# ---------------------------- NUTRITIONIX ---------------------------- #

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(
    nutritionix_endpoint,
    json=exercise_params,
    headers=headers
)

result = response.json()

# ---------------------------- DATE & TIME ---------------------------- #

today = datetime.now().strftime("%d/%m/%Y")
now = datetime.now().strftime("%H:%M:%S")

# ---------------------------- SHEETY ---------------------------- #

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

for exercise in result["exercises"]:

    sheet_inputs = {
        "workout": {
            "date": today,
            "time": now,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(
        SHEETY_ENDPOINT,
        json=sheet_inputs,
        headers=sheety_headers
    )

    print(sheet_response.text)