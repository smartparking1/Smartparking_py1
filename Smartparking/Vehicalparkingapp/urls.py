from django.urls import path
from .views import *

urlpatterns = [
    path('insertvehicleparking/',InsertVehicleParking.as_view(),name='insertvehicleparking'),
    path('updatevehicleparking/<int:empId>/',UpdateVehicleParking.as_view(),name='updatevehicleparking'),
    path('updatefineamount/',UpdateFineAmount.as_view(),name='updatefineamount')
]