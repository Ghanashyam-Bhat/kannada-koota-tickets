from django.urls import path,re_path
from . import views

urlpatterns = [
    path('status/',views.login_status),
    path('login/',views.login_api),
    path('logout/',views.logout_api),
    re_path(r'^proxy/(.*)$', views.proxy_handler),
]