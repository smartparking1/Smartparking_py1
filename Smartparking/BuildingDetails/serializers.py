from .models import *
from rest_framework import serializers
from django.core.files.images import get_image_dimensions
from django.utils.encoding import smart_str
from django.conf import settings
import logging



class FloorSerializer(serializers.ModelSerializer) :
    # building = BuildingSerializer()
    class Meta :
        model = FloorDetails
        fields = '__all__'
    
class FloorsDetailsSerializer(serializers.ModelSerializer):
    # building = BuildingSerializer(read_only=True)

    class Meta:
        model = FloorDetails
        fields = '__all__'


class SlotSerializer(serializers.ModelSerializer):
    floor = FloorSerializer()
    class Meta:
        model = SlotDetails
        fields = '__all__'
    
    def create(self, validated_data):
        floor_data = validated_data.pop('floor')
        building_data = floor_data.pop('building')
        building = BuildingDetails.objects.create(**building_data)
        floor = FloorDetails.objects.create(building=building,**floor_data)
        slot = SlotDetails.objects.create(floor=floor,**floor_data)
        return slot
    
class SlotDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotDetails
        fields = '__all__'

    def update(self, instance, validated_data):
        # Update the fields of SlotDetails instance
        instance.status = validated_data.get('status', instance.status)
       
        # Save the updated SlotDetails instance
        instance.save()
        return instance
    


#* building serilizers

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingDetails
        fields = ['building_id', 'building_name', 'location', 'status', 'images', 'no_of_floors']

   
    
