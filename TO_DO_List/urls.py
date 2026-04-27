from django.urls import path
from .views import *

urlpatterns = [
    path('lists/', get_all_lists),
    path('lists/<str:list_name>/', get_items_in_list),
    path('lists/create/', create_list_view),
    path('lists/delete/', delete_list_view),

    path('todo/add/', add_todo_view),
    path('todo/delete/', delete_todo_view),
    path('todo/update/', update_todo_view),
]