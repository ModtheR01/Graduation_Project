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
    url = "https://skyscanner-flights-travel-api.p.rapidapi.com/flights/searchAirport"

    params = {
        "query": query,
        "market": "US",
        "locale": "en-US"
    }

    response = requests.get(url, headers=HEADERS, params=params)
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

    return {
        "skyId": best["skyId"],
        "entityId": best["entityId"]
    }


@tool
def search_flights(origin: str, destination: str, date: str):
    """
    Search for available flights between two cities on a given date.

    Inputs:
    - origin: departure city name (e.g., "London" or "Cairo")
    - destination: arrival city name (e.g., "New York")
    - date: travel date in format YYYY-MM-DD

    Returns:
    - A list of top 5 flights with key information:
        - route (from → to)
        - departure and arrival time
        - duration
        - price
        - airline
        - whether the flight is direct

    Notes:
    - City names can be in English or Arabic (they will be normalized).
    - Results are simplified and optimized for display and AI understanding.
    """
    #print("in tool")
    origin_ids = get_place_id(origin)
    dest_ids = get_place_id(destination)

    if not origin_ids or not dest_ids:
        return {"error": "Invalid location"}

    url = "https://skyscanner-flights-travel-api.p.rapidapi.com/flights/searchFlights"

    params = {
        "originSkyId": origin_ids["skyId"],
        "destinationSkyId": dest_ids["skyId"],
        "originEntityId": origin_ids["entityId"],
        "destinationEntityId": dest_ids["entityId"],
        "date": date,
        "adults": "1",
        "cabinClass": "economy",
        "currency": "USD",
        "market": "US"
    }

    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()

    flights = []

    for item in data.get("itineraries", [])[:5]:
        leg = item["legs"][0]

        # 🧠 تحويل duration
        hours = leg["durationMinutes"] // 60
        minutes = leg["durationMinutes"] % 60

        flights.append({
            "route": f"{origin} → {destination}",
            "time": f"{leg['departure'][11:16]} → {leg['arrival'][11:16]}",
            "duration": f"{hours}h {minutes}m",
            "price": f"${int(item['price']['amount'])}",
            "airline": leg["carriers"][0]["name"],
            "direct": leg["stopCount"] == 0,
            #"booking_url": item["bookingUrl"]
        })

    return {
        "count": len(flights),
        "flights": flights
    }
# from datetime import datetime
# from urllib import response
# import requests , time
# from chat.api_keys import Amadeus_BaseURL, Amadeus_Key, Amadeus_SecretKey


# _TOKEN={"token": None,"expires_at":0} # _TOKEN -> name convention to assume it as a private var only in this file , all letter uper case because it is a constant
# def get_access_token(client_id, client_secret):
#     now = time.time() 
#     if _TOKEN["token"] and _TOKEN["expires_at"] > now + 30:   # 30 seconds
#         return  _TOKEN["token"]
#     token_url = f"{Amadeus_BaseURL}/v1/security/oauth2/token"
#     response = requests.post(token_url, data={
#         "grant_type":"client_credentials",
#         "client_id":client_id, 
#         "client_secret":client_secret
#     }, timeout=20)
#     response.raise_for_status() # if the status code of response not (200-299) , the exception will be through
#     json=response.json()
#     token = json.get("access_token")
#     if not token:
#         raise ValueError("Access token missing in response")
#     _TOKEN["token"] = token
#     _TOKEN["expires_at"] = now + int(json.get("expires_in", 1800)) # 1800 -> 30 min
#     return token

# def search_flights(origin, destination, date):
#     # print("in func")
#     search_url=f"{Amadeus_BaseURL}/v2/shopping/flight-offers"
#     token=get_access_token(Amadeus_Key,Amadeus_SecretKey)
#     headers={"Authorization": f"Bearer {token}"}
#     params={
#         "originLocationCode": origin,
#         "destinationLocationCode": destination,
#         "departureDate": date,
#         "adults": 1,  # عدد البالغين (مطلوب)
#         "currencyCode": "USD",  # اختياري: لتحديد العملة
#         "max": 4  # اختياري: عدد النتائج المرجعة (الحد الأقصى 250)
#     }
#     response=requests.get(search_url,headers=headers,params=params,timeout=30)
#     print("STATUS:", response.status_code)
#     print("RESPONSE:", response.text)
#     return response.json()

# def normalize_date(date_str: str) -> str:
#     formats = [
#         "%Y-%m-%d",   # 2026-01-01
#         "%d/%m/%Y",   # 01/01/2026
#         "%d-%m-%Y",   # 01-01-2026
#     ]

#     for fmt in formats:
#         try:
#             return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
#         except ValueError:
#             continue

#     raise ValueError("Invalid date format")

# def flight_offer_price(offer): # This API is used to validate and confirm the flight price before booking.
#     price_url=f"{Amadeus_BaseURL}/v1/shopping/flight-offers/pricing"
#     token=get_access_token(Amadeus_Key,Amadeus_SecretKey)
#     headers={
#         "Authorization": f"Bearer {token}",  # Bearer  -> type of authentication
#         "Content-Type" : "application/json"  # Type of data will be sent
#         }
#     # payload -> # put the selected offer in the correct format
#     payload={
#                 "data": {
#                     "type": "flight-offers-pricing",
#                     "flightOffers": [offer]
#                 }
#             }
#     response= requests.post(price_url,json=payload,headers=headers,timeout=10)
#     response.raise_for_status()
#     return response.json()



# if __name__ == "__main__":
#     result = search_flights("CAI", "RUH", "2026-04-20")
#     print(result)
