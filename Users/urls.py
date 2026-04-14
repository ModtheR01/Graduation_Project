from django.urls import path
from . import views

urlpatterns=[
    path("signup/",views.signup),
    path("login/",views.login),
    path("logingoogle/",views.login_with_google),
]