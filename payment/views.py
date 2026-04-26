import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from chat.api_keys import Stripe_Secret, Stripe_Webhook_Secret
from flights.models import Traveling
from flights.state_store import get_store
from Tasks.models import Tasks
from flights.utilities import generate_ticket_number
from datetime import datetime
from Hotels.models import Hotels
from Hotels.utils import generate_booking_number

stripe.api_key = Stripe_Secret

@csrf_exempt
def stripe_webhook(request):
    payload = request.body #data sent by stripe to our webhook endpoint when a payment event occurs
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event( #to check it is a valid event sent by stripe and not a fake request, it will raise an error if the signature is invalid or if the payload is malformed
            payload, sig_header, Stripe_Webhook_Secret
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400) # هنخلي 400 عشان ده معناه ان في حد بيحاول يبعت طلبات مزورة لويب هوك بتاعنا
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "payment_intent.succeeded": # This event is triggered when a payment is successfully completed. It contains information about the payment, including the metadata we attached when creating the PaymentIntent.
        payment_intent = event["data"]["object"]
        payment_intent_dict = payment_intent.to_dict()
        task_id = payment_intent_dict.get("metadata", {}).get("task_id")
        if not task_id:
            return HttpResponse(status=200)
        try:
            task = Tasks.objects.get(id=task_id)
        except Tasks.DoesNotExist:
            return HttpResponse(status=404)
        if task.task_type == "flight_booking":
            flight = task.offer_data
            time_str = flight.get("time", " → ")
            parts = time_str.split(" → ")
            departure_time = parts[0] if len(parts) > 0 else None
            return_time = parts[1] if len(parts) > 1 else None
            date_str = flight.get("date", "")
            ticket_num = generate_ticket_number()
            while Traveling.objects.filter(ticket_num=ticket_num).exists():
                ticket_num = generate_ticket_number()
            try:
                traveling, created = Traveling.objects.get_or_create(
                    task_id=task.id,
                    defaults={
                        "ticket_num": ticket_num,
                        "origin": flight.get("route", "").split(" → ")[0],
                        "destination": flight.get("route", "").split(" → ")[-1],
                        "departure_date": date_str,
                        "departure_time": departure_time,
                        "return_time": return_time,
                        "number_of_passengers": 1,
                        "moving_method": "Flight",
                        "moving_service_provider": flight.get("airline", "Unknown"),
                    }
                )
                if not created:
                    return HttpResponse(status=200)  # Already exists, no need to create again
            except Exception as e:
                print("Error creating Traveling record:", e)
                return HttpResponse(status=500)
            # if task.booking_data:
            #     task.booking_data["status"] = "confirmed"
            #     task.save()
            print("✅ Payment confirmed for task:", task_id)

        elif task.task_type == "hotel_booking":
            hotel = task.booking_data.get("hotel", {})
            booking_data = task.booking_data
            
            booking_number = generate_booking_number()  
            while Hotels.objects.filter(booking_number=booking_number).exists():
                booking_number = generate_booking_number()
            try:
                hotel_record, created = Hotels.objects.get_or_create(
                    task_id=task.id,
                    defaults={
                        "booking_number": booking_number,
                        "hotel_name": hotel.get("name"),
                        "number_of_persons": booking_data.get("hotel", {}).get("num_of_adults"),
                        "number_of_rooms": booking_data.get("hotel", {}).get("num_of_rooms"),
                        "check_in_date": hotel.get("booking_info", {}).get("checkin_from"),
                        "check_out_date": hotel.get("booking_info", {}).get("checkout_from"),
                    }
                )
                if not created:
                    return HttpResponse(status=200)
            except Exception as e:
                print("Error creating Hotel record:", e)
                return HttpResponse(status=500)
        task.booking_data["status"] = "confirmed"
        task.save()

    return HttpResponse(status=200)