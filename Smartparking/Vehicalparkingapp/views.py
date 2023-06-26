from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from .models import *
from .serializer import *

class VehicalIn(GenericAPIView,CreateModelMixin):
    queryset=VehicleParking.objects.all()
    serializer_class=VehicalSerilizer
    def  post(self,request):
        print("ok")
        print(request.data)
        return self.create(request)
        
class VhecalOut(GenericAPIView,RetrieveModelMixin):
    queryset = VehicleParking.objects.all()
    serializer_class = VehicalSerilizer
    def get(self,request,no):
        print(no)

        vehical=VehicleParking.objects.filter(vehicle_no=no)
        print(vehical)
        serializer=VehicalSerilizer(data=vehical,many=True)
        serializer.is_valid()
        return Response(serializer.data)
