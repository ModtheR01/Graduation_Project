from django.shortcuts import render

# Create your views here.
import requests , os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv

load_dotenv()


@api_view(['GET'])
def get_hotels(request):
    url = "https://booking119.p.rapidapi.com/api/v1/hotels/searchHotels"

    headers = {
        "x-rapidapi-key": "ec70cef473mshdd9e129ed168a66p13aea3jsn7eed8a1136e3",
        "x-rapidapi-host": "booking119.p.rapidapi.com"
    }

    params = {
        "dest_id": "-1456928",
        "search_type": "CITY",
        "arrival_date": "2026-05-26",
        "departure_date": "2026-05-29"
    }

    response = requests.get(url, headers=headers, params=params)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    data = response.json()

    hotels = data.get("data", {}).get("hotels", [])

    if not hotels:
        return Response({
            "message": "No hotels found",
            "raw_response": data
        })

    hotels_list = []

    for hotel in hotels:
        hotels_list.append({
            "name": hotel["property"]["name"],
            "price": hotel["property"]["priceBreakdown"]["grossPrice"]["value"],
            "rating": hotel["property"]["reviewScore"],
            "image": hotel["property"]["photoUrls"][0]
        })

    return Response(hotels_list)
