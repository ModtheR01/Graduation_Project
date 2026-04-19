import stripe
from chat.api_keys import Stripe_Secret

stripe.api_key = Stripe_Secret

def create_payment_intent(booking,task_id):
    price = booking["price"]
    flight = booking["flight"]
    email = booking["user"]["email"]
    price = int(price.replace("$","").replace(",","")) * 100 # Remove the dollar sign and convert to cents "Because Stripe expects the price in cents"

    intent = stripe.PaymentIntent.create(
        amount=price,
        currency="usd",
        receipt_email=email,
        automatic_payment_methods={
            "enabled": True,
            "allow_redirects": "never",  # 👈 الحل هنا
        },
        metadata={
            "task_id": str(task_id),
            "email": email,
            "route": flight.get("route", ""),
        },
        description=f"Flight {flight.get('route', '')}",
    )

    return intent.client_secret ,intent.id