import requests
from datetime import datetime

# ---------------------------- USER DETAILS ------------------------------- #
print("Reached line 1")

USERNAME = "manoghna123"
TOKEN = "manoghna2026secret"

GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

# ---------------------------- CREATE USER ------------------------------- #
print("creating user")
user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

#Uncomment ONLY the first time you run it
response = requests.post(url=pixela_endpoint, json=user_params)
print(response.text)
print(response.status_code)

# ---------------------------- CREATE GRAPH ------------------------------- #

# graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

# graph_config = {
#     "id": GRAPH_ID,
#     "name": "Coding Graph",
#     "unit": "hours",
#     "type": "float",
#     "color": "ajisai"
# }

# headers = {
#     "X-USER-TOKEN": TOKEN
# }


# # Uncomment ONLY the first time you create the graph
# response = requests.post(
#      url=graph_endpoint,
#      json=graph_config,
#      headers=headers )
# print(response.text)

# ---------------------------- ADD PIXEL ------------------------------- #
# print(__file__)
# today = datetime.now()

# pixel_endpoint = (
#     f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
# )

# pixel_data = {
#     "date": today.strftime("%Y%m%d"),
#     "quantity": input("How many hours did you code today? ")
# }

# response = requests.post(
#     url=pixel_endpoint,
#     json=pixel_data,
#     headers=headers
# )

# print(response.text)

# ---------------------------- UPDATE PIXEL ------------------------------- #

# update_endpoint = (
#     f"{pixela_endpoint}/{USERNAME}/graphs/"
#     f"{GRAPH_ID}/{today.strftime('%Y%m%d')}"
# )
#
# update_data = {
#     "quantity": "5"
# }
#
# response = requests.put(
#     url=update_endpoint,
#     json=update_data,
#     headers=headers
# )
#
# print(response.text)

# ---------------------------- DELETE PIXEL ------------------------------- #

# delete_endpoint = (
#     f"{pixela_endpoint}/{USERNAME}/graphs/"
#     f"{GRAPH_ID}/{today.strftime('%Y%m%d')}"
# )
#
# response = requests.delete(
#     url=delete_endpoint,
#     headers=headers
# )
#
# print(response.text)