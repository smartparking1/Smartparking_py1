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
        time = datetime.now().time()  # Define the desired time
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
        vehicleparkingdata = VehicleParking.objects.filter(vehicle_no=vehicleNo.get('vehicle_no'))
        for vehicle_data in vehicleparkingdata:
            if vehicle_data.checkout_time is None:
                date = datetime.now().date()  # Get the current date
                time = datetime.now().time()  # Get the current time
                combined_datetime = datetime.combine(date, time)
                vehicle_data.checkout_time = combined_datetime
                try:
                    vehicle = EmployeeDetails.objects.get(id=empId)
                    vehicle_data.checkout_by = vehicle
                except ObjectDoesNotExist:
                    return Response("Invalid check-in by ID", status=status.HTTP_400_BAD_REQUEST)
                vehicle_data.save()
                
            else:
                print('not ok')
        # vehicle_data = VehicleParking.objects.filter(vehicle_no=vehicleNo.get('vehicle_no'))
        serializer_data = VehicleParkingSerializer(data=vehicleparkingdata,many=True)
        serializer_data.is_valid()
        return Response((serializer_data.data)[vehicleparkingdata.count()-1])

        
class UpdateFineAmount(APIView):
    def put(self,request):
        serializer = VehicleParkingSerializer(data = request.data)
        serializer.is_valid()
        vehicle_data = serializer.data
        vehicleParking = VehicleParking.objects.filter(vehicle_no = vehicle_data.get('vehicle_no'))
        for vehicle_data in vehicleParking :
            if vehicle_data.checkout_time is None :
                vehicle_data.fine_amount = vehicle_data.get('fine_amount')
                vehicle_data.total_amount = vehicle_data.parking_amount + vehicle_data.fine_amount
                vehicle_data.save()

        return Response("Saved successfully", status=status.HTTP_201_CREATED)

class GetAllVehicles(GenericAPIView,ListModelMixin) :
    queryset = VehicleParking.objects.all()
    serializer_class = VehicleParkingSerializer

    def get(self,request) :
        return self.list(request)