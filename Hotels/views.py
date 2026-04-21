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
    - arr_date (str): Check-in date. (always make the date in this format YYYY-MM-DD)
    - dep_date (str): Check-out date. (always make the date in this format YYYY-MM-DD) 
    - num_of_adults (int): Number of adults.
    - num_of_rooms (int): Number of rooms.
    Notes:
    - The function ALWAYS returns this exact Python dict structure.
    - "images" will always contain exactly 2 image URLs.
    - Date format is flexible in separators ("-", "/", "."),
        but MUST follow: day → month → year (DD-MM-YYYY).

    You must follow this format when return the response:(you never ignore ant thing in this format)
        Here are the available hotels in Cairo from 24/04/2026 to 05/05/2026:
        | # | Hotel Name | Rating | Price | Stars | Check-in | Check-out | Images |
        |---|------------|--------|-------|-------|----------|-----------|--------|
        | 1 | LA Cairo Plaza Hotel | 10.0 | 73.72 USD | ⭐⭐⭐⭐⭐ | 10:00 → 12:00 | 11:00 → 13:00 | [Img1](https://cf.bstatic.com/image1.jpg), [Img2](https://cf.bstatic.com/image2.jpg) |
        | 2 | Nile View Hotel | 8.5 | 55.00 USD | ⭐⭐⭐⭐ | 14:00 → 23:00 | 06:00 → 12:00 | [Img1](https://cf.bstatic.com/image3.jpg), [Img2](https://cf.bstatic.com/image4.jpg) |
        Would you like to book any of these hotels? Just let me know which one!
    """
    try:
        info_of_hotels = func_search_hotels(country,arr_date,dep_date,num_of_adults,num_of_rooms)
        if not info_of_hotels:
            return "no hotels found"
        return f"[FINAL_ANSWER]{info_of_hotels}"
    except Exception as e:
        return f"message: {str(e)}"

