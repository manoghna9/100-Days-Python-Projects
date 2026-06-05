class FlightSearch:
    city_codes = {
        "Paris": "PAR",
        "Berlin": "BER",
        "Tokyo": "TYO",
        "Sydney": "SYD",
    }

    def get_destination_code(self, city_name):
        return self.city_codes[city_name]