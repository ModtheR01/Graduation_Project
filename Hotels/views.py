from langchain_core.tools import tool
from Hotels.utils import func_search_hotels
from Hotels.state_store import get_store
from Tasks.models import Tasks
from django.utils import timezone
from payment.utils import create_payment_intent_hotels
import stripe
import traceback

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
    print("in hotel search")
    try:
        info_of_hotels = func_search_hotels(country,arr_date,dep_date,num_of_adults,num_of_rooms)
        if not info_of_hotels:
            return "no hotels found"
        return f"[FINAL_ANSWER]{info_of_hotels}"
    except Exception as e:
        print(f"Hotel search error: {e}")  # ← أضف ده
        traceback.print_exc()  # ← ده هيوريك السطر بالظبط
        return f"message: {str(e)}"

@tool
def booking_hotel(offer_id:int,Fname:str,Lname:str,gender:str,BD:str,national_id_num:int,email:str,phone_number:str,nationality:str):
    """
        book a hotel offer by its ID from the last search results.
        IMPORTANT: If the tool returns [PAYMENT_REQUIRED], return ONLY this text as-is:
        "Your booking is ready! The Payment will appear here, Please complete the payment."
        Do NOT add any other text or explanation.
    """
    store=get_store()
    offer = store.get("last_offers", {}).get(offer_id) 

    if not offer:
        return {"error": "Invalid offer ID"}
    print("SELECTED OFFER:", offer)

    booking = {
        "hotel": offer,
        "price": offer["price"],
        "user": {
            "fname": Fname,
            "lname": Lname,
            "gender": gender,
            "birth_date": BD,
            "email": email,
            "phone": phone_number,
            "nationality": nationality,
            "national id number" : national_id_num
        },
        "status": "pending"
    }

    chat_id = store.get("chat_id") # in view of chat we store the chat_id in state store after creating a new chat or getting an existing one
    task=Tasks.objects.create(
        chat_id=chat_id,
        task_type="hotel_booking",
        created_at=timezone.now(),       
        booking_data=booking,  
    )

    try:
        client_secret , payment_intent_id = create_payment_intent_hotels(booking,task.id)
        task.booking_data["payment_intent_id"] = payment_intent_id
        task.booking_data["client_secret"] = client_secret 
        task.save()
        store["pending_payment_task_id"] = task.id
        return "[PAYMENT_REQUIRED]"
    except stripe.error.AuthenticationError:
        task.delete()
        return {"error": "Payment system configuration error."}
    except stripe.error.InvalidRequestError as e:
        task.delete()
        return {"error": f"Invalid payment data: {e}"}
    except stripe.error.APIConnectionError:
        task.delete()
        return {"error": "Cannot connect to payment provider. Try again."}
    except stripe.error.StripeError as e:
        task.delete()
        return {"error": "Payment error. Please try again."}
    except (AttributeError, KeyError) as e:
        task.delete()
        return {"error": "Booking data is incomplete."}
