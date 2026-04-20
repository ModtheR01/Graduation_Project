from asyncio import Task
from django.utils import timezone
from urllib import response
from django.http import JsonResponse
import requests
from langchain_core.tools import tool
import stripe
from flights.state_store import get_store
from chat.api_keys import XRapidAPIKey
from .utilities import get_place_id
from payment.utils import create_payment_intent
from Tasks.models import Tasks
from flights.models import Traveling

print("in views")
HEADERS = {
    "x-rapidapi-key": XRapidAPIKey,
    "x-rapidapi-host": "skyscanner-flights-travel-api.p.rapidapi.com"
}


@tool
def search_flights(origin: str, destination: str, date: str):
    """
    Always communicate with the user in the same language they use, and respond in that language.
    Search for available flights between two cities on a given date.
    Input Rules:
        origin: departure city name (ANY language is allowed), if the user doesn't mention the name of city and mention the name of nation, you can use the nation's capital as the origin city.
            The system MUST convert it to English before processing.
        destination: arrival city name (ANY language is allowed), if the user doesn't mention the name of city and mention the name of nation, you can use the nation's capital as the origin city.
            The system MUST convert it to English before processing.
        date: travel date in format YYYY-MM-DD , if the user provides it in another format, convert it to the required format before processing.
    Important Notes:
        Always assume user input may be misspelled or not in English.
    Output Rules (STRICT FORMAT):
        - You MUST call the tool and return its response as-is.
        - The flight results are considered RAW DATA.
        You MUST NOT translate, reformat, summarize, or modify them in any way.
        - Even if the user speaks Arabic, DO NOT translate airline names, times, prices, or formatting.
        - If the tool output starts with [FINAL_ANSWER], you MUST return everything after it EXACTLY as-is.
        - The language rule applies ONLY to normal conversation text, NOT to structured flight results.
    """
    print("🔥 search_flights CALLED")
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

    for i, item in enumerate(data.get("itineraries", [])[:5], 1):
        leg = item["legs"][0]
        # 🧠 تحويل duration
        hours = leg["durationMinutes"] // 60
        minutes = leg["durationMinutes"] % 60
        flights.append({
            "id": i,
            "route": f"{origin} → {destination}",
            "date": date,
            "time": f"{leg['departure'][11:16]} → {leg['arrival'][11:16]}",
            "duration": f"{hours}h {minutes}m",
            "price": f"${int(item['price']['amount'])}",
            "airline": leg["carriers"][0]["name"],
            "direct": leg["stopCount"] == 0,
            "stops": leg["stopCount"]
        })
    if not flights:
        return "[FINAL_ANSWER]\nNo flights found for this route/date."
    flights_text = f"{origin} → {destination} | {date}\n"
    for i, f in enumerate(flights, 1):
        stops = "Direct" if f["direct"] else f"{f['stops']} Stop(s)"
        flights_text += f"""{f['airline']}
        {f['time']}  ({f['duration']})
        {f['price']}
        {stops}
        """
    
    store = get_store()
    store["last_offers"] = {f["id"]: f for f in flights}
    print("ALL OFFERS:", store["last_offers"].get(2))
    print("TOOL RESULT:", flights_text)
    return f"[FINAL_ANSWER]{flights}"


# if __name__ == "__main__":
#     print(search_flights("Cairo", "Riyadh", "2026-05-10"))

@tool
def booking_flight(offer_id:int,Fname:str,Lname:str,gender:str,BD:str,email:str,phone_number:str,passport_num:str,passport_expire_date:str,nationality:str):
    """
        book a flight offer by its ID from the last search results.
        IMPORTANT: If the tool returns [PAYMENT_REQUIRED], return ONLY this text as-is:
        "Your booking is ready! The Payment will appear here, Please complete the payment."
        Do NOT add any other text or explanation.
    """
    print("in booking tool in views")
    store= get_store()
    offer = store.get("last_offers", {}).get(offer_id)  # Safely get the selected offer:- If "last_offers" exists → use it- If not → use empty dict {} to avoid crash- Then try to get offer_id → returns None if not found (no error)

    if not offer:
        return {"error": "Invalid offer ID"}
    print("SELECTED OFFER:", offer)

    booking = {
        "flight": offer,
        "price": offer["price"],
        "user": {
            "fname": Fname,
            "lname": Lname,
            "gender": gender,
            "birth_date": BD,
            "email": email,
            "phone": phone_number,
            "passport": passport_num,
            "passport_expire": passport_expire_date,
            "nationality": nationality
        },
        "status": "pending"
    }

    chat_id = store.get("chat_id") # in view of chat we store the chat_id in state store after creating a new chat or getting an existing one
    task=Tasks.objects.create(
        chat_id=chat_id,
        task_type="flight_booking",
        created_at=timezone.now(),
        offer_data=offer,        
        booking_data=booking,  
    )

    try:
        client_secret , payment_intent_id = create_payment_intent(booking, task_id=task.id)
        task.booking_data["payment_intent_id"] = payment_intent_id
        task.booking_data["client_secret"] = client_secret 
        task.save()
        store["pending_payment_task_id"] = task.id # we store the pending payment task id in state store to retrieve it in the chat view
        print("Payment intent created with client_secret:", client_secret)
        print("task created with ID:", task.id)
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



def get_ticket(request):
    task_id = request.GET.get("task_id")

    if not task_id:
        return JsonResponse({"error": "task_id is required"}, status=400)

    try:
        task = Tasks.objects.get(id=task_id)
    except Tasks.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if task.booking_data.get("status") != "confirmed":
        payment_intent_id = task.booking_data.get("payment_intent_id")

        if not payment_intent_id:
            return JsonResponse({"error": "Payment not initiated"}, status=400)

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if intent.status == "succeeded":
                task.booking_data["status"] = "confirmed"
                task.save()
        except stripe.error.StripeError:
            return JsonResponse({"error": "Could not verify payment"}, status=500)

    if task.booking_data.get("status") != "confirmed":
        return JsonResponse({"error": "Payment not confirmed yet"}, status=402)

    flight = task.offer_data
    booking = task.booking_data

    traveling = Traveling.objects.filter(task_id=task.id).first()
    if not traveling:
        return JsonResponse({"error": "Ticket not ready yet"}, status=404)

    return JsonResponse({
        "ticket": {
            "passenger": {
                "fname": booking["user"].get("fname"),
                "lname": booking["user"].get("lname"),
                "gender": booking["user"].get("gender"),
                "passport": booking["user"].get("passport"),
                "nationality": booking["user"].get("nationality"),
            },
            "flight": {
                "ticket_number": traveling.ticket_num,
                "airline": flight.get("airline"),
                "route": flight.get("route"),
                "date": flight.get("date"),
                "time": flight.get("time"),
                "price": flight.get("price"),
            },
            "status": booking.get("status"),
        }
    })




# def test_payment(request):
#     booking = {
#         "flight": {
#             "route": "Cairo → Dubai",
#             "price": "$120",
#             "airline": "Emirates",
#             "date": "22/12/2026",
#             "time": "10:00 → 14:00"
#         },
#         "price": "$120",
#         "user": {
#             "fname": "Test",
#             "lname": "User",
#             "email": "test@test.com",
#             "passport": "A123456",
#             "gender": "Male",
#             "nationality": "Egyptian",
#             "phone": "01012345678",
#             "birth_date": "1990-01-01",
#         },
#         "status": "pending"
#     }

#     task = Tasks.objects.create(
#         chat_id=1,
#         task_type="flight_booking",
#         created_at=timezone.now(),
#         offer_data=booking["flight"],
#         booking_data=booking
#     )

#     client_secret, payment_intent_id = create_payment_intent(booking, task_id=task.id)
#     task.booking_data["payment_intent_id"] = payment_intent_id
#     task.save()  # ✅ ناقصة

#     return JsonResponse({
#         "task_id": task.id,
#         "client_secret": client_secret,
#         "payment_intent_id": payment_intent_id
#     })














# @tool
# def search_anywhere(origin: str):
#     """
#     Get cheapest destinations from a city
#     """

#     def get_place(city):
#         url = "https://skyscanner-flights.p.rapidapi.com/flights/searchAirport"
#         res = requests.get(url, headers=HEADERS, params={"query": city})
#         data = res.json()

#         if data.get("places"):
#             p = data["places"][0]
#             return p["skyId"], p["entityId"]
#         return None, None

#     origin_sky, origin_entity = get_place(origin)

#     url = "https://skyscanner-flights.p.rapidapi.com/flights/searchFlightEverywhere"

#     res = requests.get(url, headers=HEADERS, params={
#         "originSkyId": origin_sky,
#         "originEntityId": origin_entity
#     })

#     data = res.json()

#     results = []
#     for d in data.get("destinations", [])[:5]:
#         results.append({
#             "city": d["name"],
#             "country": d["countryName"],
#             "price": d["price"]
#         })

#     return results






































# @tool
# def search_for_flights(origin: str, destination: str, date: str):
#     """
#         Search for available flight offers between two cities on a specific date.
#         This tool MUST be used whenever the user provides enough information to search for flights.

#         to call this tool:
#         - The user specifies an origin city or airport (e.g., Cairo, CAI)
#         - The user specifies a destination city or airport (e.g., Riyadh, RUH)
#         - The user provides a travel date

#         Important behavior rules:
#         - ALWAYS call this tool once the origin, destination, and date are known.
#         - DO NOT ask for confirmation if all required information is already provided.
#         - If the user confirms (e.g., says "yes"), proceed with the search immediately.
#         - Convert city names to IATA airport codes if needed (e.g., Cairo → CAI, Riyadh → RUH).
#         - Convert the date to YYYY-MM-DD format before calling the tool.

#     Formatting rules (VERY IMPORTANT):
#         - Always format responses in a clean, human-readable way.
#         - Avoid using raw newline characters like "\n" in the final output.
#         - Use clear line breaks and spacing as if writing a message to a user.
#         - Present flight results as a numbered list with each flight on a separate line.
#         - Do NOT return escaped characters (e.g., "\n", "\t").
#         - Ensure the output looks natural and well-structured in chat interfaces.
#         Example format:
#         1. Flight ID: 1 | Airline: F3 | Departure: 02:35 → Arrival: 05:20 | Price: 107 USD
#         2. Flight ID: 2 | Airline: XY | Departure: 10:50 → Arrival: 13:35 | Price: 123 USD

#         After calling this tool:
#         - You MUST present the flight options clearly to the user
#         - Then ask the user to choose an offer_id to proceed with booking
#         """
#     try:
#         date = normalize_date(date)
#     except ValueError:
#         return {"error": "Invalid date format. Use DD/MM/YYYY or YYYY-MM-DD."}

#     try:
#         flights = search_flights(origin, destination, date)
#         if "data" not in flights or not flights["data"]:
#             return f"No flights found from {origin} to {destination} on {date}."
#         text = f"Flights from {origin} to {destination} on {date}:\n\n"
#         for i, f in enumerate(flights["data"][:5], 1):
#             text += (
#                 f"{i}. Flight ID: {f['id']} | "
#                 f"Airline: {f['validatingAirlineCodes'][0]} | "
#                 f"Price: {f['price']['total']} {f['price']['currency']}\n"
#             )
#         flights["data"].sort(key=lambda x: float(x["price"]["total"]))
#         get_store()["last_offers"] = {offer["id"]: offer for offer in flights["data"]}
#         return text
#     except Exception as e:
#         return {"error": str(e)}

# @tool
# def prepare_payment_for_offer(offer_id: str,Fname,Lname,gender,BD,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality):
#     """
#     Book a selected flight offer using its ID from the last search results.

#     This tool should be called ONLY after:
#     1. A flight search has been performed using search_for_flights.
#     2. The user has selected a flight offer by its ID.

#     The tool automatically validates the selected offer price 
#     by calling the pricing endpoint before creating the booking.

#     Parameters:
#         offer_id (str): The ID of the flight offer chosen by the user 
#         from the previously displayed search results.

#         Fname (str): Passenger first name (uppercase recommended).
#         Lname (str): Passenger last name.
#         gender (str): Passenger gender ("MALE" or "FEMALE").
#         BD (str): Passenger date of birth in YYYY-MM-DD format.
#         email (str): Passenger email address.
#         county_calling_code (str): Phone country calling code (e.g., "20" for Egypt).
#         phone_number (str): Passenger mobile number.
#         passport_num (str): Passport number.
#         passport_expire_date (str): Passport expiry date in YYYY-MM-DD format.
#         passport_issuance_country (str): Country issuing the passport (2-letter ISO code).
#         nationality (str): Passenger nationality (2-letter ISO code).

#     Returns:
#         JSON response from Amadeus containing the booking confirmation 
#         and PNR if the booking is successful.

#     Notes:
#         - The flight offer is automatically price-validated before booking.
#         - If the offer ID is invalid or no previous search exists, 
#         the booking will fail.
#     """

#     # catch offers has been searched before and stored in state store by search_for_flights tool
#     offers = get_store()["last_offers"]
#     if not offers:
#         return {"error": "No previous search found. Please search again."}
#     # select specific offer by its ID from the stored offers
#     selected_offer = offers.get(offer_id)
#     if not selected_offer:
#         return {"error": "Invalid offer ID. Please search again."}

#     try:
#         # return the final price of the selected offer after validating it by calling the pricing API
#         priced_data = flight_offer_price(selected_offer)
#     except Exception as e:
#         return {"error": str(e)}

#     final_offer = priced_data["data"]["flightOffers"][0]
#     amount = float(final_offer["price"]["total"])
#     currency = final_offer["price"]["currency"]

#     store = get_store()
#     store["passenger_data"] = {
#         "Fname": Fname,
#         "Lname": Lname,
#         "gender": gender,
#         "BD": BD,
#         "email": email,
#         "county_calling_code": county_calling_code,
#         "phone_number": phone_number,
#         "passport_num": passport_num,
#         "passport_expire_date": passport_expire_date,
#         "passport_issuance_country": passport_issuance_country,
#         "nationality": nationality
#     }
#     store["final_offer"] = final_offer

#     return {
#         "status": "awaiting_payment",
#         "amount": amount,
#         "currency": currency,
#         "message": f"Total price is {amount} {currency}. Please complete payment."
#     }

# def flight(final_offer, Fname, Lname, gender, BD, email, county_calling_code, phone_number, passport_num, passport_expire_date, passport_issuance_country, nationality):

#     price_url=f"{Amadeus_BaseURL}/v1/booking/flight-orders"
#     token=get_access_token(Amadeus_Key,Amadeus_SecretKey)
#     priced_offer = final_offer
#     headers={
#         "Authorization": f"Bearer {token}",  
#         "Content-Type" : "application/json"
#         }
#     payload={
#                 "data": {
#                     "type": "flight-order",
#                     "flightOffers": [
#                     priced_offer
#                     ],
#                     "travelers": [
#                     {
#                         "id": "1",
#                         "dateOfBirth": BD ,
#                         "gender": gender,
#                         "name": {
#                         "firstName":Fname ,
#                         "lastName": Lname
#                         },
#                         "contact": {
#                         "emailAddress": email ,
#                         "phones": [
#                             {
#                             "deviceType": "MOBILE",
#                             "countryCallingCode": county_calling_code,
#                             "number": phone_number
#                             }
#                         ]
#                         },
#                         "documents": [
#                         {
#                             "documentType": "PASSPORT",
#                             "number": passport_num,
#                             "expiryDate": passport_expire_date,
#                             "issuanceCountry": passport_issuance_country,
#                             "nationality": nationality,
#                             "holder": True
#                         }
#                         ]
#                     }
#                     ]
#                 }
#             }
#     response= requests.post(price_url,json=payload,headers=headers,timeout=30)
#     if response.status_code != 201:
#         print("STATUS:", response.status_code)
#         print("RESPONSE:", response.text)
#         return {"error": response.text}
#     return response.json()





# flights = search_for_flights("CAI", "DXB", "2026-03-25")
# pricing_response = price_offer_by_index(1)
# priced_offer = pricing_response
# birth_data="1990-01-01"
# gender="MALE"
# Fname="JOHN"
# Lname="DOE"
# email="john@example.com"
# county_calling_code="20"
# phone_number="01012345678"
# passport_num="A12345678"
# passport_expire_date="2030-01-01"
# passport_issuance_country="EG"
# nationality="EG"
# print(flight_order(1,Fname,Lname,gender,birth_data,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality))




