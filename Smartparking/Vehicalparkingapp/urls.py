from django.urls import path
from .views import *

urlpatterns = [
    path('VehicalIn/',VehicalIn.as_view(),name='EmployeeRegister'),
    path('VhecalOut/<str:no>/',VhecalOut.as_view(),name='EmployeeRegister'),
   
]
