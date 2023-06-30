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
        print(vehicle_data)
        # Retrieve the object matching the vehicle number
        vehicle = get_object_or_404(VehicleParking, vehicle_no=vehicle_data['vehicle_no'])
        print(vehicle.vehicle_type)
       
        slipsize = (350, 250)

        

        
        print(vehicle.vehicle_type)
    
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pay_slip.pdf"'
        c = canvas.Canvas(response, pagesize=portrait(slipsize))
        c.setFont("Helvetica", 12)
        c.drawString(10, 310, "----------------- PAY SLIP -----------------")
        c.drawString(10, 290, f"vehicle No    : {vehicle.vehicle_no}")
        c.drawString(10, 270, f"vehicle type  : {vehicle.vehicle_type}")
        c.drawString(10, 250, f"checkin time  : {vehicle.checkin_time}")
        c.drawString(10, 230, f"checkout time : {vehicle.checkout_time}")
        c.drawString(10, 210, f"parking_amount: {vehicle.parking_amount}")
        c.drawString(10, 190, f"fine_amount   : {vehicle.fine_amount}")
        c.drawString(10, 160, "----------------- total -----------------")
        c.drawString(10, 140, f"total_amount  : {vehicle.total_amount}")
        c.drawString(10, 100, "----------------- THANK YOU -----------------")
        c.save()

        return response



