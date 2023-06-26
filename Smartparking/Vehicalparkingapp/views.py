from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin
from .serializer import *
from .models import *
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

# Create your views here.



class InsertVehicleParking(GenericAPIView, CreateModelMixin):
    queryset = VehicleParking.objects.all()
    serializer_class = VehicleParkingSerializer
   
    def post(self, request):
        serializer = VehicleParkingSerializer(data=request.data)
        serializer.is_valid()
        vehicleparking = serializer.data
         
        date = datetime.now().date()  # Get the current date
        time = datetime.strptime("12:30:00", "%H:%M:%S").time()  # Define the desired time
        combined_datetime = datetime.combine(date, time)
        
        vehicle_parking = VehicleParking()
        vehicle_parking.vehicle_no = vehicleparking.get('vehicle_no')
        vehicle_parking.vehicle_type = vehicleparking.get('vehicle_type')
        vehicle_parking.checkin_time = combined_datetime
        vehicle_parking.parking_amount = vehicleparking.get('parking_amount')
        vehicle_parking.fine_amount = vehicleparking.get('fine_amount')
        vehicle_parking.total_amount = vehicle_parking.parking_amount + vehicle_parking.fine_amount
        
        try:
            slot = SlotDetails.objects.get(slot_id=vehicleparking.get('slot'))
            vehicle_parking.slot = slot
        except ObjectDoesNotExist:
            return Response("Invalid slot ID", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            vehicle = EmployeeDetails.objects.get(id=vehicleparking.get('checkin_by'))
            vehicle_parking.checkin_by = vehicle
        except ObjectDoesNotExist:
            return Response("Invalid check-in by ID", status=status.HTTP_400_BAD_REQUEST)
        
        vehicle_parking.save()
        return Response("Saved successfully", status=status.HTTP_201_CREATED)
    
class UpdateVehicleParking(APIView):
    def put(self,request,empId) :
        serializer = VehicleParkingSerializer(data = request.data)
        serializer.is_valid()
        vehicleNo  = serializer.data
        vehicleparkingdata = VehicleParking.objects.get(vehicle_no=vehicleNo.get('vehicle_no'))
        date = datetime.now().date()  # Get the current date
        time = datetime.strptime("12:30:00", "%H:%M:%S").time()  # Define the desired time
        combined_datetime = datetime.combine(date, time)
        vehicleparkingdata.checkout_time = combined_datetime

        try:
            vehicle = EmployeeDetails.objects.get(id=empId)
            vehicleparkingdata.checkout_by = vehicle
        except ObjectDoesNotExist:
            return Response("Invalid check-in by ID", status=status.HTTP_400_BAD_REQUEST)
        
        vehicleparkingdata.save()
        return Response("Saved successfully", status=status.HTTP_201_CREATED)

        
class UpdateFineAmount(APIView):
    def put(self,request):
        serializer = VehicleParkingSerializer(data = request.data)
        serializer.is_valid()
        vehicle_data = serializer.data
        vehicleParking = VehicleParking.objects.get(vehicle_no = vehicle_data.get('vehicle_no'))
        vehicleParking.fine_amount = vehicle_data.get('fine_amount')
        vehicleParking.total_amount = vehicleParking.parking_amount + vehicleParking.fine_amount
        vehicleParking.save()
        return Response("Saved successfully", status=status.HTTP_201_CREATED)