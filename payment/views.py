# payment/views.py

import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from flights.state_store import get_store   # عدل حسب مكان الملف
# from flights.views import flight            # عدل حسب مكان الفانكشن
from chat.api_keys import Stripe_Webhook_Secret
@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = Stripe_Webhook_Secret

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    # 🔥 الكود بتاعك هنا
    if event["type"] == "payment_intent.succeeded":

        print("PAYMENT SUCCESS")

        store = get_store()

        final_offer = store.get("final_offer")
        passenger_data = store.get("passenger_data")

        if not final_offer or not passenger_data:
            print("Missing data!")
            return HttpResponse(status=400)

        result = flight(final_offer, **passenger_data)

        print("Booking result:", result)

    return HttpResponse(status=200)