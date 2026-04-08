from django.urls import path
from . import views

urlpatterns=[
    path("contact/",views.contact_list),
    path("contact/create/",views.contact_create),
    path("contact/update/<int:pk>/",views.contact_update),
    path("contact/delete/<int:pk>/",views.contact_delete),
]