from django.urls import path
from . import views

urlpatterns=[
    path("chat/",views.send_message),
    path("get_user_chats/",views.get_user_chats),
    path("get_chat_by_id/<int:chat_id>/",views.get_chat_by_id),
    path("delete_chat/<int:chat_id>/",views.delete_chat),
]