import requests

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self, access_token):
        self.access_token = access_token
        self.flight_search_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        self.location_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations"
        self.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    def flight_search(self, origin, destination, departure_date):
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": 1,
            "currencyCode": "USD",
            "max": 1
        }

        response = requests.get(
            url=self.flight_search_endpoint,
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_iata_code(self, city_name):
        params = {"subType": "CITY", "keyword": city_name}

        response = requests.get(self.location_endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data["data"]:  # if Amadeus returns at least 1 city
            return data["data"][0]["iataCode"]
        else:
            return None  # city not found

    def update_iata_code(self, row_id, iata_code):
        new_data = {
            "price": {
                "iataCode": iata_code
            }
        }

        requests.put(
            url=f"{SHEETY_ENDPOINT}/{row_id}",
            json=new_data,
            headers=self.headers
        )
