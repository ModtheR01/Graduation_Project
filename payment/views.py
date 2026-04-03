from django.shortcuts import render
import stripe
import json
from django.http import JsonResponse, HttpResponse
import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
#from Core.Flights.tools import flight


load_dotenv()

# stripe.api_key= Stripe_Secret
# endpoint_secret=Stripe_Webhook_Secret

Stripe_Secret=os.getenv("STRIPE_SECRET")
Stripe_Webhook_Secret=os.getenv("STRIPE_WEBHOOK_SECRET")
stripe.api_key=Stripe_Secret

def create_payment_intent(request):
    data = json.loads(request.body)
    amount = data["amount"]
    intent=stripe.PaymentIntent.create(
        amount= amount,
        currency="usd",
        automatic_payment_methods={"enabled": True},
        metadata={
            "flight_index": data["index"],
            "email": data["email"]
    }
    )
    if request.method != "POST": # create-payment -> only receive requests with method "POST"
        return HttpResponse(status=405)
    return JsonResponse({"clientSecret": intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload=request.body
    signature = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event=stripe.Webhook.construct_event(
            payload=payload,
            sig_header=signature,
            secret=Stripe_Webhook_Secret
        )
    except stripe.error.SignatureVerificationError as e:
        print("Signature error:", e)
        return HttpResponse(status=400)
    except ValueError as e:
        print("Payload error:", e)
        return HttpResponse(status=400)
    print("Event type:", event["type"])
    
    if event['type'] == "payment_intent.succeeded" :
        payment_intent = event["data"]["object"]   # to catch full data sent by PaymentIntent in object, this_object => contains some keys (metadata,status,amount,...)
        flight_index  = payment_intent["metadata"]["flight_index"] # from the object catch metadata to catch "flight_index"
        email =  payment_intent["email"]
        print("PAYMENT SUCCESS")
        print("Flight : ",flight_index )
        print("Email : ",email)
        flight()

    elif event['type'] == "payment_intent.payment_failed" :
        print("PAYMENT FAILED")

    return HttpResponse(status=200)