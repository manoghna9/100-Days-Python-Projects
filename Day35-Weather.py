import requests

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = "cf7a4c11e6b47fc2965124265b6a935e"

weather_params = {"lat": 12.9716,"lon": 77.5946,"appid": api_key,"cnt": 4,}

response = requests.get(OWM_Endpoint,params=weather_params)

response.raise_for_status()
weather_data = response.json()
print(weather_data)

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    print("Bring an umbrella")
else:
    print("No rain today")