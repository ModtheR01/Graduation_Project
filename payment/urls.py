from django.urls import path
from . import views

urlpatterns=[
    path("webhook/stripe/",views.stripe_webhook)
]