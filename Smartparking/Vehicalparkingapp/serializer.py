from rest_framework import serializers
from .models import *
from employee_authentication.models import *
from BuildingDetails.models import *

class VehicalSerilizer(serializers.ModelSerializer):
    slot=SlotDetails()
    employe=EmployeeDetails()
    


    class Meta:
        model = VehicleParking
        fields = '__all__'
    
    # def create(self, validated_data):
    #     slot_data = validated_data.pop('slot')
    #     slot = BuildingDetails.objects.filter(**slot_data).first()
    #     employee_data=validated_data.pop('chekin_by')
    #     chekin_employee= EmployeeDetails.objects.filter(**employee_data).first()
    #     vehicle_parking =VehicleParking.objects.create(
    #         slot=slot,chekin_by=chekin_employee,**validated_data)
    #     return vehicle_parking