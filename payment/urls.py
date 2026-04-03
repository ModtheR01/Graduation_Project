from django.urls import path
from . import views

urlpatterns=[
    path("create-payment-intent/",views.create_payment_intent),
    path("webhook/",views.stripe_webhook)
]