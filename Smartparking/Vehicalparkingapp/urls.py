from django.urls import path
from .views import *

urlpatterns = [
    path('insertvehicleparking/',InsertVehicleParking.as_view(),name='insertvehicleparking'),
    path('updatevehicleparking/<int:empId>/<str:vehicle_no>/',UpdateVehicleParking.as_view(),name='updatevehicleparking'),
    path('updatefineamount/',UpdateFineAmount.as_view(),name='updatefineamount'),
    path('getallvehicleparking/',GetAllVehicles.as_view(),name='getallvehicleparking'),
]