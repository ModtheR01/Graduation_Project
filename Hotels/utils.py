from chat.api_keys import XRapidAPIKey
import requests


print("in utilities")
HEADERS = {
    "x-rapidapi-key": XRapidAPIKey,
    "x-rapidapi-host": 'booking-com15.p.rapidapi.com'
}

def get_dest_id(query: str):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"

    params = {
        "query": query,
        "locale": "en-us"
    }

    response = requests.get(url, headers=HEADERS, params=params)

    print("status code:", response.status_code)
    print("response:", response.text[:500])

    data = response.json()

    places = data.get("data", [])  # ✅ الصح

    if not places:
        return None

    best = places[0]

    return {
        "dest_id": best.get("dest_id"),
        "dest_type": best.get("dest_type")
    }


def func_search_hotels(country,arr_date,dep_date,num_of_adults,num_of_rooms):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"

    headers = {
        "X-RapidAPI-Key": XRapidAPIKey,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }
    dest=get_dest_id(country)
    dest_id=dest["dest_id"]
    dest_type=dest["dest_type"]

    params = {
        "dest_id": dest_id,
        "search_type": dest_type.upper(),  # 🔥 مهم
        "arrival_date":arr_date ,           #"2026-05-01"
        "departure_date": dep_date,              #"2026-05-05",
        "adults": num_of_adults,
        "room_qty": num_of_rooms,
        "page_number": 1,
        "languagecode": "en-us",
        "currency_code": "USD"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    hotels = data.get("data", {}).get("hotels", [])

    result = []

    for h in hotels:
        p = h.get("property", {})

        images = p.get("photoUrls", [])
        if len(images) >= 2:
            selected_images = images[:2]
        elif len(images) == 1:
            selected_images = [images[0], images[0]]
        else:
            selected_images = [
                "https://via.placeholder.com/300",
                "https://via.placeholder.com/300"
            ]

        hotel = {
            "id": h.get("hotel_id"),
            "name": p.get("name"),
            "rating": p.get("reviewScore"),
            "price": p.get("priceBreakdown", {}).get("grossPrice", {}).get("value"),
            "currency": p.get("priceBreakdown", {}).get("grossPrice", {}).get("currency"),
            "images": selected_images,
            "stars": p.get("propertyClass"),
            "booking_info": {
                "checkin_from": p.get("checkin", {}).get("fromTime"),
                "checkin_until": p.get("checkin", {}).get("untilTime"),
                "checkout_from": p.get("checkout", {}).get("fromTime"),
                "checkout_until": p.get("checkout", {}).get("untilTime"),
            }
        }

        result.append(hotel)

    
    print("status:", response.status_code)
    print("result from tool:",result )
    #print(result)

    return result


print(func_search_hotels("cairo","2026-05-01","2026-05-05",2,1))