import requests
from langchain_core.tools import tool
from flights.state_store import get_store
from chat.api_keys import XRapidAPIKey
print("in utilities")
HEADERS = {
    "x-rapidapi-key": XRapidAPIKey,
    "x-rapidapi-host": "skyscanner-flights-travel-api.p.rapidapi.com"
}

def get_place_id(query: str):
    print("in get place id")
    print("XRapidAPIKey:", XRapidAPIKey)
    url = "https://skyscanner-flights-travel-api.p.rapidapi.com/flights/searchAirport"

    params = {
        "query": query,
        "market": "US",
        "locale": "en-US"
    }
    print("calling flights API...")
    response = requests.get(url, headers=HEADERS, params=params)
    print("status code:", response.status_code)
    print("response:", response.text[:500])
    data = response.json()

    places = data.get("places", [])

    if not places:
        return None

    # 🎯 exact match الأول
    exact = next(
        (p for p in places if p["name"].lower() == query.lower()),
        None
    )

    if exact:
        best = exact
    else:
        # fallback
        city = next((p for p in places if p["placeType"] == "CITY"), None)
        airport = next((p for p in places if p["placeType"] == "AIRPORT"), None)
        best = city if city else airport
    print(f"get_place_id('{query}') -> {best['name']} ({best['skyId']})")
    return {
        "skyId": best["skyId"],
        "entityId": best["entityId"]
    }

# def generate_ticket_number():
#     from datetime import datetime
#     import random

#     year = datetime.now().year
#     random_num = random.randint(100000, 999999)

#     return f"FL-{year}-{random_num}"

# if __name__ == "__main__":
#     result = search_flights("CAI", "RUH", "2026-04-20")
#     print(result)
