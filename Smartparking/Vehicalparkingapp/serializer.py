from rest_framework import serializers
from .models import *

class VehicleParkingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VehicleParking
        fields = '__all__'

class Priceserializer(serializers.ModelSerializer):
    
    class Meta:
        model=Prices
        fields = '__all__'