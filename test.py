import requests

response = requests.get(
    "https://www.google.com",
    timeout=5
)

print(response.status_code)
