import requests
import os

SHEETY_ENDPOINT = "https://api.sheety.co/0941799fbc65fd731bdc98717c24435f/flightDeal/prices"
SHEETY_TOKEN = "abdullohabdulvadud"

class DataManager:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {SHEETY_TOKEN}"
        }

    def get_destination_data(self):
        response = requests.get(
            url=SHEETY_ENDPOINT,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["prices"]

    def update_iata_code(self, row_id, iata_code):
        new_data = {
            "price": {
                "iataCode": iata_code
            }
        }

        response = requests.put(
            url=f"{SHEETY_ENDPOINT}/{row_id}",
            json=new_data,
            headers=self.headers
        )
        response.raise_for_status()
        

    def get_all_data(self):
        response = requests.get(
            url=SHEETY_ENDPOINT,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()["prices"]
