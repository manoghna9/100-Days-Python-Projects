import requests

SHEETY_ENDPOINT = "https://api.sheety.co/7b8cb3ebb12c41d15fbf6258c835ea31/flightFinder/sheet1"

class DataManager:

    def __init__(self):
        self.destination_data = []

    def get_destination_data(self):
        response = requests.get(SHEETY_ENDPOINT)
        data = response.json()
        return data["sheet1"]  # or data["prices"]
    
        return self.destination_data
    
    def update_destination_codes(self):
        print("Updating destination codes...")

        for city in self.destination_data:

            new_data = {
                "sheet1": {
                    "iataCode": city["iataCode"]
                }
            }

            response=requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.status_code)
            print(response.text)

    