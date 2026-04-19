from django.urls import path
from . import views

urlpatterns=[
    path("success/get_ticket/",views.get_ticket),
    #path("test_payment/",views.test_payment),
]