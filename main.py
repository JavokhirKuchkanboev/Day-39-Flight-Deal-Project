import requests
from flight_search import FlightSearch
from data_manager import DataManager

# 1️⃣ Create DataManager
data_manager = DataManager()

# 2️⃣ Amadeus token
AMADEUS_API_KEY = "jseMpGqtcAPaBYqkb5AJigtHsZ5AOJyB"
AMADEUS_KEY_SECRET = "AmRackeWGp6BglDW"

token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "client_credentials",
    "client_id": AMADEUS_API_KEY,
    "client_secret": AMADEUS_KEY_SECRET
}

response = requests.post(token_endpoint, headers=headers, data=data)
response.raise_for_status()
access_token = response.json()["access_token"]

# 3️⃣ Create FlightSearch object
flight_search = FlightSearch(access_token=access_token)

# 4️⃣ Read Google Sheet
sheet_data = data_manager.get_all_data()

# 5️⃣ Update missing IATA codes
for row in sheet_data:
    if not row["iataCode"]:
        city = row["city"]
        row_id = row["id"]

        iata_code = flight_search.get_iata_code(city)
        if iata_code:
            data_manager.update_iata_code(row_id, iata_code)
            row["iataCode"] = iata_code
            print(f"{city} → {iata_code} updated")
        else:
            print(f"{city} → IATA code not found")
