from django.http import FileResponse, JsonResponse
from .models import *

import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *

from rest_framework.views import APIView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from Vehicalparkingapp.serializer import VehicleParkingSerializer

from Vehicalparkingapp.models import VehicleParking

from django.shortcuts import get_object_or_404
from Vehicalparkingapp.models import VehicleParking

from reportlab.lib.pagesizes import portrait



class GetVehicledetails(GenericAPIView,RetrieveModelMixin):
       queryset=VehicleParking.objects.all()
       serializer_class=VehicleParkingSerializer

       def post(self, request):
        vehicle_data = request.data
        vehicle=VehicleParking.objects.filter(vehicle_no=vehicle_data['vehicle_no']).last()
        slipsize = (350, 250)
        time_difference = (vehicle.checkout_time.time().hour-vehicle.checkin_time.time().hour)+((vehicle.checkout_time.time().minute-vehicle.checkin_time.time().minute)/100)
       #  time_difference=
    
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pay_slip.pdf"'
        c = canvas.Canvas(response, pagesize=portrait(slipsize))
        c.setFont("Helvetica", 12)
        c.drawString(10, 310, "----------------- PAY SLIP -----------------")
        c.drawString(10, 290, f"Vehicle No    : {vehicle.vehicle_no}")
        c.drawString(10, 270, f"Vehicle type  : {vehicle.vehicle_type}")
        c.drawString(10, 250, f"Checkin time  : {vehicle.checkin_time}")
        c.drawString(10, 230, f"Checkout time : {vehicle.checkout_time}")
        c.drawString(10, 210, f"Total time    : {time_difference}")
        c.drawString(10, 190, f" Parking amount: {vehicle.parking_amount}")
        c.drawString(10, 160, f"Fine amount   : {vehicle.fine_amount}")
        c.drawString(10, 140, "----------------- total -----------------")
        c.drawString(10, 100, f"Total amount  : {vehicle.total_amount}")
        c.drawString(10, 70, "----------------- THANK YOU -----------------")
        c.save()

        return response



