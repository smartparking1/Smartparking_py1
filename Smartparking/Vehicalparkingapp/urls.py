from django.urls import path
from .views import *

urlpatterns = [
    path('insertvehicleparking/',InsertVehicleParking.as_view(),name='insertvehicleparking'),
    path('PriceInsert/',PriceInsert.as_view(),name='PriceInsert'),
    path('PriceGetting/',PriceGetting.as_view(),name='PriceGetting'),
    path('updatevehicleparking/<int:empId>/<str:vehicle_no>/',UpdateVehicleParking.as_view(),name='updatevehicleparking'),
    path('PriceUpadate/<int:id>/',PriceUpadate.as_view(),name='updatevehicleparking'),
    path('updatefineamount/',UpdateFineAmount.as_view(),name='updatefineamount'),
    path('getallvehicleparking/',GetAllVehicles.as_view(),name='getallvehicleparking'),
]
