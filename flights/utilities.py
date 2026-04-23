import random
import json
from datetime import datetime, timedelta
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import requests
from langchain_core.tools import tool
from flights.state_store import get_store
from chat.api_keys import XRapidAPIKey

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

def generate_ticket_number():
    year = datetime.now().year
    random_num = random.randint(100000, 999999)

    return f"FL-{year}-{random_num}"


geolocator = Nominatim(user_agent="romee_app")

_coordinates_cache = {}

def get_coordinates(city: str):
    if city in _coordinates_cache:
        return _coordinates_cache[city]
    try:
        location = geolocator.geocode(city)
        if not location:
            return None
        coords = (location.latitude, location.longitude) # latitude -> خطوط الطول
        _coordinates_cache[city] = coords
        return coords
    except Exception:
        return None

def calculate_distance(origin: str, destination: str):
    origin_coords = get_coordinates(origin)
    dest_coords = get_coordinates(destination)
    if not origin_coords or not dest_coords:
        return None
    return geodesic(origin_coords, dest_coords).km

def calculate_arrival(departure_time: str, duration_hours: float):
    dep = datetime.strptime(departure_time, "%H:%M")
    arr = dep + timedelta(hours=duration_hours)
    return arr.strftime("%H:%M")

def generate_mock_flights(origin: str, destination: str, date: str):
    print("Mock Flights")
    distance = calculate_distance(origin, destination)
    if not distance:
        return []

    # السعر بناءً على المسافة
    base_price = max(90, distance * 0.12)

    # المدة بناءً على المسافة
    duration_hours = (distance / 900) + 0.5

    airlines = [
        "EgyptAir",
        "Emirates",
        "Air Arabia",
        "Lufthansa",
        "Turkish Airlines",
        "flydubai",
    ]

    departure_times = random.sample(
        [f"{h:02d}:00" for h in [6, 8, 10, 12, 14, 16, 18, 20, 22]], 5
    )

    flights = []
    for i, (airline, dep_time) in enumerate(zip(airlines, departure_times), 1):
        price_variation = random.uniform(0.85, 1.35)
        stops = random.choices([0, 1], weights=[80, 20])[0]
        actual_duration = duration_hours + (1.5 if stops else 0)
        hours = int(actual_duration)
        minutes = int((actual_duration % 1) * 60)

        flights.append({
            "id": i,
            "route": f"{origin} → {destination}",
            "date": date,
            "airline": airline,
            "time": f"{dep_time} → {calculate_arrival(dep_time, actual_duration)}",  # ✅ نفس الـ real
            "duration": f"{hours}h {minutes}m",
            "price": f"${int(base_price * price_variation)}",
            "stops": stops,
            "direct": stops == 0,
        })

    return flights

#print(generate_mock_flights("Cairo","Dubai","25/4/2026"))
