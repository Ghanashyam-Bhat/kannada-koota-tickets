from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.ticketSubmissions),
    # path("batchUpload/", views.massUpload),
]
