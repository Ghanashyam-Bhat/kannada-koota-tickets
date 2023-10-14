from django.urls import path 
from . import views

urlpatterns = [
    path('status/',views.login_status),
    path('login/',views.login_api),
    path('logout/',views.logout_api),
]