from django.shortcuts import render

# Create your views here.
import requests , os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv
from langchain_core.tools import tool
from Hotels.utils import func_search_hotels

load_dotenv()

@tool
def search_hotels(country,arr_date,dep_date,num_of_adults,num_of_rooms):
    """
    Search for available hotels in a given city/country within a date range.

    Parameters:
    - country (str): Name of the city or country (e.g., "Cairo", "Paris").
    - arr_date (str): Check-in date.
    - dep_date (str): Check-out date.
    - num_of_adults (int): Number of adults.
    - num_of_rooms (int): Number of rooms.

    Returns:
    - A Python dictionary with the following fixed structure:

        {
            "status": "success",
            "data": [
                {
                    "id": int,
                    "name": str,
                    "rating": float,
                    "price": float,
                    "currency": str,
                    "images": list[str],   # always 2 image URLs
                    "stars": int,
                    "booking_info": {
                        "checkin_from": str,
                        "checkin_until": str,
                        "checkout_from": str,
                        "checkout_until": str
                    }
                }
            ]
        }

    Notes:
    - The function ALWAYS returns this exact Python dict structure.
    - "images" will always contain exactly 2 image URLs.
    - Date format is flexible in separators ("-", "/", "."),
        but MUST follow: day → month → year (DD-MM-YYYY).

    Example:
        {
            "status": "success",
            "data": [
                {
                    "id": 16134399,
                    "name": "LA Cairo Plaza Hotel",
                    "rating": 10.0,
                    "price": 73.72,
                    "currency": "USD",
                    "images": [
                        "https://cf.bstatic.com/image1.jpg",
                        "https://cf.bstatic.com/image2.jpg"
                    ],
                    "stars": 5,
                    "booking_info": {
                        "checkin_from": "10:00",
                        "checkin_until": "12:00",
                        "checkout_from": "11:00",
                        "checkout_until": "13:00"
                    }
                }
            ]
        }
    """
    try:
        info_of_hotels = func_search_hotels(country,arr_date,dep_date,num_of_adults,num_of_rooms)
        if not info_of_hotels:
            return {
                "status": "error",
                "message": "No hotels found",
                "data": []  
            }
        return {
            "status": "success",   
            "data": info_of_hotels
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []   # ✅ ثابت
        }
