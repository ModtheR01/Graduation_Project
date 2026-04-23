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
from chat.models import Chats
from flights.utilities import generate_mock_flights


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
        you must follow this format in english
            "Here are the available flights from Cairo to Casablanca on 24/4/2026:\n\n| # | Route | Date | Time | Duration | Price | Airline | Direct |\n|---|-------|------|------|----------|-------|---------|--------|\n| 1 | Cairo → Casablanca | 2026-04-24 | 09:00 → 12:30 | 5h 30m | $465 | EgyptAir | ✅ Yes |\n| 2 | Cairo → Casablanca | 2026-04-24 | 16:20 → 00:20 | 10h 0m | $326 | Lufthansa | ❌ 1 stop |\n| 3 | Cairo → Casablanca | 2026-04-24 | 09:40 → 13:30 | 5h 50m | $453 | Royal Air Maroc | ✅ Yes |\n Would you like to book any of these flights? Just let me know which one!"
        you must follow this format in arabic
            "            إليك الرحلات المتاحة بناءً على طلبك:

            | # | المسار | التاريخ | الوقت | المدة | السعر | شركة الطيران | التوقفات |
            |---|-------|---------|-------|-------|-------|-------------|--------|
            | 1 | القاهرة → باريس | 2026-05-05 | 04:45 → 13:45 | 10h 0m | $419 | Lufthansa | توقفان |
            | 2 | القاهرة → باريس | 2026-05-05 | 03:10 → 09:50 | 7h 40m | $344 | LOT | توقف واحد |
            | 3 | القاهرة → باريس | 2026-05-05 | 17:35 → 20:00 | 27h 25m | $442 | Emirates | مباشر |

            - 🏆 **الأسرع (Fastest):** Emirates
            - 💰 **الأرخص (Cheapest):** LOT 
            - ✨ **الأفضل (Best):** Lufthansa

            هل تود حجز أي من هذه الرحلات؟"
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

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        flights = []
        for i, item in enumerate(data.get("itineraries", [])[:5], 1):
            leg = item["legs"][0]
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
    except Exception as e:
        print(f"API Error: {e}")
        flights = []

    if not flights:
        print("Using mock flights...")
        flights = generate_mock_flights(origin, destination, date)



    # flights_text = f"{origin} → {destination} | {date}\n"
    # for i, f in enumerate(flights, 1):
    #     stops = "Direct" if f["direct"] else f"{f['stops']} Stop(s)"
    #     flights_text += f"""{f['airline']}
    #     {f['time']}  ({f['duration']})
    #     {f['price']}
    #     {stops}
    #     """
    #print("ALL OFFERS:", store["last_offers"].get(2))
    #print("TOOL RESULT:", flights_text)

    store = get_store()
    store["last_offers"] = {f["id"]: f for f in flights}
    return f"[FINAL_ANSWER]{flights}"


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
    traveling = Traveling.objects.filter(task_id=int(task_id)).first()

    if not traveling:
        print("Ticket not ready yet")
        return JsonResponse({"error": "Ticket not ready yet"}, status=404)

    message={
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
    }
    chat_id = task.chat_id
    chat = Chats.objects.filter(id=chat_id).first()
    if chat:
        print("chat exist")
        messages = chat.message or []
        messages.append({
            "role": "assistant",
            "content": message
        })
        chat.message = messages
        chat.save()

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

