import requests

SHEETY_ENDPOINT = "https://api.sheety.co/7b8cb3ebb12c41d15fbf6258c835ea31/flightFinder/sheet1"

response = requests.get(SHEETY_ENDPOINT)

print(response.status_code)
print(response.json())