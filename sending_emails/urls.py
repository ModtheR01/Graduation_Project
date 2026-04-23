from django.urls import path
from . import views

urlpatterns=[
    path("contact/",views.contact_list),
    path("contact/create/",views.contact_create),
    path("contact/update/<int:pk>/",views.contact_update),
    path("contact/delete/<int:pk>/",views.contact_delete),
    path("google-auth-url/",views.get_google_auth_url),  # hassan call this to get google api to call
    path("oauth2callback/",views.google_callback),
    path("is-connected/",views.is_connected),
    path("disconnect/",views.disconnect),


]