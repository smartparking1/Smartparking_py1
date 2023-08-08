from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin,UpdateModelMixin,RetrieveModelMixin,DestroyModelMixin
from .serializer import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from .exception import *
import math
from .service import *
import datetime
from django.http import JsonResponse
from rest_framework.permissions import  IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import permission_classes




class InsertVehicleParking(GenericAPIView, CreateModelMixin):
    queryset = VehicleParking.objects.all()
    serializer_class = VehicleParkingSerializer
   
    def post(self, request):
        serializer = VehicleParkingSerializer(data=request.data)
        serializer.is_valid()
        vehicleparking = serializer.data
         
        date = datetime.datetime.now().date()  # Get the current date
        time = datetime.datetime.now().time()  # Define the desired time
        combined_datetime = datetime.datetime.combine(date, time)
        
        vehicle_parking = VehicleParking()
        vehicle_parking.vehicle_no = vehicleparking.get('vehicle_no')
        vehicle_parking.vehicle_type = vehicleparking.get('vehicle_type')
        vehicle_parking.checkin_time = combined_datetime
        vehicle_parking.parking_amount = int( gettingpriceByslotId(vehicleparking.get('slot'),vehicle_parking.vehicle_type,date))
       
        vehicle_parking.fine_amount = vehicleparking.get('fine_amount')
        vehicle_parking.total_amount = vehicle_parking.parking_amount + vehicle_parking.fine_amount
        checkingCar(vehicle_parking.vehicle_no)
        try:
            slot = SlotDetails.objects.get(slot_id=vehicleparking.get('slot'))
            vehicle_parking.slot = slot
        except ObjectDoesNotExist:
            
            return Response("Invalid slot ID", status=status.HTTP_400_BAD_REQUEST)
        try:
            employee = EmployeeDetails.objects.get(id=vehicleparking.get('checkin_by'))
            vehicle_parking.checkin_by = employee
        
        except ObjectDoesNotExist:
            return Response("Invalid check-in by ID", status=status.HTTP_400_BAD_REQUEST)
        
        vehicle_parking.save()
        return Response("Saved successfully", status=status.HTTP_201_CREATED)
    
class UpdateVehicleParking(APIView):
    def put(self,request,empId,vehicle_no) :
        serializer = VehicleParkingSerializer(data = request.data)
        serializer.is_valid()
        vehicleNo  = serializer.data
        vehicleparkingdata = VehicleParking.objects.filter(vehicle_no=vehicle_no,checkout_time=None)
        print(vehicleparkingdata,'-------------------------------')
        try:
            if(len(vehicleparkingdata)==0):
                raise VehicleNotFound('Please enter the currect details')
            else:
                for vehicle_data in vehicleparkingdata:
                    if vehicle_data.checkout_time is None:
                        date = datetime.datetime.now().date()  # Get the current date
                        time = datetime.datetime.now().time()  # Get the current time
                        combined_datetime = datetime.datetime.combine(date, time)
                        vehicle_data.checkout_time = combined_datetime
                        if (vehicle_data.checkout_time.time().hour-vehicle_data.checkin_time.time().hour) > 0:

                            start_date = vehicle_data.checkin_time  #starting Date
                            end_date = vehicle_data.checkout_time   # Checkouttime
                            hours_per_day = {}
                            current_date = vehicle_data.checkin_time.date()


    
                            while current_date<=end_date.date():
                                if current_date == start_date.date():
                                        hours = 24 - start_date.hour
                                elif current_date == end_date.date():
                                        hours = end_date.hour
                                else:
                                    hours = 24
                                hours_per_day[current_date] = hours
                                current_date += datetime.timedelta(days=1)
                            print(hours_per_day,'''''''''dvfdvdvdvdvdvdvdvdvdvdv''''''''''''''''')

                            total_time=0
                            total_days=0
                            for day,hours in hours_per_day.items():
                                total_time+=hours
                                total_days+=1
                            print(total_days,total_time ,"0000000000000000000000000000000")
                                                    
                            vehicle_data.total_amount = calulatingamout(hours_per_day,vehicle_data.slot,vehicle_data.vehicle_type)  
                        else :
                            vehicle_data.total_amount = vehicle_data.total_amount
                        try:
                            employee = EmployeeDetails.objects.get(id=empId)
                            vehicle_data.checkout_by = employee
                        except ObjectDoesNotExist:
                            return Response("Invalid check-in by ID", status=status.HTTP_400_BAD_REQUEST)
                        vehicle_data.save()
                        serializer_data = VehicleParkingSerializer(data=vehicleparkingdata,many=True)
                        serializer_data.is_valid()
                        return Response((serializer_data.data)[vehicleparkingdata.count()-1])
                        
                else:
                    raise VehicleNotFound("Vehicle not found")
        except VehicleNotFound as v:
            return JsonResponse({'error': str(v)}, status=400)

        
        
class UpdateFineAmount(APIView):
    def put(self,request):
        serializer = VehicleParkingSerializer(data = request.data)
        serializer.is_valid()
        vehicle_data = serializer.data
        vehicleParking = VehicleParking.objects.filter(vehicle_no = vehicle_data.get('vehicle_no'))
        for vehicledata in vehicleParking :
            if vehicledata.checkout_time is None :
                vehicledata.fine_amount = vehicle_data.get('fine_amount')
                vehicledata.total_amount = vehicledata.parking_amount + vehicledata.fine_amount
                vehicledata.save()
                serializer_data = VehicleParkingSerializer(data=vehicleParking,many=True)
                serializer_data.is_valid()
                return Response((serializer_data.data)[vehicleParking.count()-1])

        return Response("Saved successfully", status=status.HTTP_201_CREATED)

class GetAllVehicles(GenericAPIView,ListModelMixin) :
    queryset = VehicleParking.objects.all()
    serializer_class = VehicleParkingSerializer

    def get(self,request) :      
        return self.list(request)
    


#* price modifications

class PriceInsert(GenericAPIView,CreateModelMixin):
    queryset=Prices.objects.all()
    serializer_class=Priceserializer
    def post(self,request):
        print(request.data)
        return self.create(request)
    

class PriceGetting(GenericAPIView,ListModelMixin):
    queryset=Prices.objects.all()
    serializer_class=Priceserializer
    
    @permission_classes([IsAuthenticated])
    def get(self,request) :      
        return self.list(request)
        

class PriceUpadate(APIView):
    def put(self,request,id):
        price = Prices.objects.get(id=id)
        print(price)
        serializer=Priceserializer(instance=price,data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)



class PriceInsert(GenericAPIView,CreateModelMixin):
    queryset=Prices.objects.all()
    serializer_class=Priceserializer
    @permission_classes([IsAuthenticated])
    def post(self,request):
        print(request.data)
        listOfPrices = Prices.objects.filter(building_id=request.data.get('building'))
        print(listOfPrices)
        count = 0
        for price in listOfPrices :
            print(price)
            if(price.day_type == request.data.get('day_type') and price.vehicle_type == request.data.get('vehicle_type')):
                count+=1
        if count == 0 :
            return self.create(request)
        try :
            raise PricesAlreadyAdded()
        except PricesAlreadyAdded:
            return JsonResponse({'error':"price already added for this vehicle type"},status=400)