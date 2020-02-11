from django.urls import path
from . import views

app_name = "miscall"

urlpatterns = [
    path('', views.index, name='index'),
    path('reqotp/',views.reqotp, name='reqotp'),
    path('verify/',views.verify, name='verify'),
]