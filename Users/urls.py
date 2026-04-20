from django.urls import path
from . import views

urlpatterns=[
    path("signup/",views.signup),
    path("login/",views.login),
    path("login/google/",views.login_with_google),
    path("user_info/",views.user_info),
    path('update_user_info/', views.update_user_info),
    path('delete_user/', views.delete_user),
    path('forgot_password/', views.forgot_password),
    path('reset_password/', views.reset_password),
]